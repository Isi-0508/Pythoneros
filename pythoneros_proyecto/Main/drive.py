from Google import Create_Service
from allauth.socialaccount.models import SocialToken
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

'''
CLIENTE = ''
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive.file']

service = Create_Service(CLIENTE, API_NAME, API_VERSION, SCOPES)
'''

# Asumiendo que tienes una instancia de servicio de la API de Drive autenticada
# (usando la librería google-api-python-client y el token del usuario)

def get_or_create_folder_id(drive_service, folder_name="Archivos de Mi App"):
    # 1. Buscar la carpeta por nombre
    query = (
        f"name='{folder_name}' and "
        "mimeType='application/vnd.google-apps.folder' and "
        "trashed=false"
    )
    
    response = drive_service.files().list(
        q=query,
        spaces='drive',
        fields='files(id)'
    ).execute()
    
    files = response.get('files', [])
    
    if files:
        # La carpeta ya existe, devuelve su ID
        return files[0].get('id')
    else:
        # 2. Si no existe, crear la carpeta
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = drive_service.files().create(
            body=file_metadata,
            fields='id'
        ).execute()
        return folder.get('id')

# Función para obtener las credenciales de Drive del usuario actual
def get_drive_credentials(user):
    """
    Obtiene el objeto Credentials de Google a partir de los tokens de allauth.
    """
    try:
        # 1. Obtener el token social de Google para el usuario
        social_token = SocialToken.objects.get(
            account__user=user,
            account__provider='google'
        )
        
        # 2. Construir el objeto Credentials
        # El token de acceso puede estar expirado, pero el refresh_token
        # permite renovarlo automáticamente.
        credentials = Credentials(
            token=social_token.token,           # Access Token actual
            refresh_token=social_token.token_secret, # ¡El Refresh Token!
            token_uri='https://oauth2.googleapis.com/token',
            client_id='TU_CLIENT_ID_DE_GOOGLE', # Usar variables de entorno aquí
            client_secret='TU_CLIENT_SECRET_DE_GOOGLE', # Usar variables de entorno aquí
            scopes=social_token.scopes          # Los scopes guardados
        )
        
        # Opcional pero recomendado: forzar una renovación si el token es viejo.
        # Esto asegura que el token se actualice en la DB si está expirado.
        if credentials.expired and credentials.refresh_token:
             credentials.refresh()
             
             # Actualizar el token en la base de datos de allauth si se refrescó
             social_token.token = credentials.token
             social_token.expires_at = credentials.expiration
             social_token.save()
        
        return credentials

    except SocialToken.DoesNotExist:
        # Manejar el caso si el usuario no tiene la cuenta de Google conectada
        return None


# Función principal para subir archivos (adaptada de tu función original)
def upload_file_to_drive(user, file_data, file_name, mime_type):
    
    # 1. Obtener las credenciales
    credentials = get_drive_credentials(user)
    if not credentials:
        raise PermissionError("El usuario no ha conectado su cuenta de Google Drive.")
        
    # 2. Conectarse a la API de Drive
    # Usamos la API de Drive v3
    drive_service = build('drive', 'v3', credentials=credentials)
    
    # 3. Obtener o crear la carpeta de destino (función que te di antes)
    # Aquí usarías la lógica que te proporcioné para obtener el folder_id
    from .utils import get_or_create_folder_id # Asumiendo que la pusiste en utils
    folder_id = get_or_create_folder_id(drive_service) 
    
    # 4. Preparar la subida
    file_metadata = {
        'name': file_name,
        'parents': [folder_id] # Especificar la carpeta de destino
    }
    
    # Convierte el objeto de archivo de Django a un MediaIoBaseUpload
    from googleapiclient.http import MediaIoBaseUpload
    import io
    media = MediaIoBaseUpload(io.BytesIO(file_data), mime_type, resumable=True)

    # 5. Ejecutar la subida
    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    
    return file.get('id')
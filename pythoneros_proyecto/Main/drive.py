from Google import Create_Service

CLIENTE = ''
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive.file']

service = Create_Service(CLIENTE, API_NAME, API_VERSION, SCOPES)

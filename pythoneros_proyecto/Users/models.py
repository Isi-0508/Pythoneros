from django.db import models

# Create your models here.
class image(models.Model):
    image=models.ImageField(default='images/default.png', upload_to='users/', verbose_name='Imagen de Perfil')
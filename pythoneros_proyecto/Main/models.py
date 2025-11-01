from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="schedule_blocks") #Asociar a un usuario
    task_name = models.CharField(max_length=100) #Texto corto
    task_desc = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)#Bool V/F

    #Time
    day = models.CharField(
        max_length=10,
        choices=[
            ("MON", "Lunes"), ("TUE", "Martes"), ("WED", "Miercoles"), ("THU", "Jueves"), ("FRI", "Viernes"), ("SAT", "Saturday"), ("SUN", "Domingo")
        ]
    )

    #Hour Half
    hour = models.CharField(max_length=5) #en formato: "00:00"
    half = models.BooleanField() #False para 00.00-00.30, True para 00.30-1.00.00

    fecha_creacion = models.DateTimeField(auto_now_add=True)#Guarda automaticamente la fecha de creación

    class Meta:
        unique_together = ('user', 'day', 'hour', 'half')
    
    def __str__(self):
        #segment = "a" if not self.half else "b"
        #return f"{self.user.username} - {self.day} {self.hour}{segment}: {self.trask_name[:15]}"
        return self.task_name
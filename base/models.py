from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Publication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=20)
    descripcion = models.TextField(max_length=200)
    puntuacion = models.CharField(max_length=2)
    estado = models.CharField(max_length=20)
    precio = models.CharField(max_length=20)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # ordenar la publicacion creada por update y created
        ordering = ['-update', '-created']

    def __str__(self):
        return str(self.nombre)

class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=11)
    tarjeta = models.CharField(max_length=10)

class Reportes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publication, on_delete=models.CASCADE)
    razon = models.TextField(max_length=200)
    estado = models.CharField(max_length=20)

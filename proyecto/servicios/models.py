from django.db import models
from django.contrib.auth.models import AbstractUser

"""
    Generic Models
"""

class Ciudad(models.Model):
    """
        Model Ciudad
    """
    nombre = models.CharField(max_length=100)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Localidad(models.Model):
    """
        Model Localidad
    """
    nombre = models.CharField(max_length=100)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.PROTECT)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Barrio(models.Model):
    """
        Model Barrio
    """
    nombre = models.CharField(max_length=100)
    localidad = models.ForeignKey(Localidad, on_delete=models.PROTECT)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
    
class UserProfile(AbstractUser):
    """
        Model Usuario Extension
    """
    telefono = models.CharField(max_length=30)
    barrio = models.ForeignKey(Barrio, on_delete=models.PROTECT)

    def __str__(self):
        return self.user.username
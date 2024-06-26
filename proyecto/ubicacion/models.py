from django.db import models

# Create your models here.
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
    ciudad = models.ForeignKey(Ciudad,on_delete = models.SET_NULL,null=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Barrio(models.Model):
    """
        Model Barrio
    """
    nombre = models.CharField(max_length=100)
    localidad = models.ForeignKey(Localidad,on_delete = models.SET_NULL,null=True)


    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
    


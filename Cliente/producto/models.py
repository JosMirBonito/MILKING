from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_categoria

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre_producto = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.nombre_producto
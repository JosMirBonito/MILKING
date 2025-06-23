from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from Cliente.pedidos.models import Pedido
from Cliente.producto.models import Producto, Categoria

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    rol = models.CharField(max_length=10)

    def __str__(self):
        return f'Usuario {self.id_usuario} - {self.rol}'

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
  # Relación uno a uno con User
    nombre_cliente = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_cliente





class Directivo(models.Model):
    id_directivo = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # <-- Añadido
    nombre_directivo = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_directivo

class OperadorSistema(models.Model):
    id_ope_sistema = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # <-- Añadido
    nombre_ope_sistema = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_ope_sistema

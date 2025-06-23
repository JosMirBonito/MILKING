from django.db import models
from Cliente.pedidos.models import Pedido

# Create your models here.

class Albaran(models.Model):
    id_albaran = models.AutoField(primary_key=True)
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name='albaran')
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    archivo = models.FileField(upload_to='albaranes/', null=True, blank=True)
    conforme = models.BooleanField(default=False)
    comentario = models.TextField(blank=True)
    fecha_conformidad = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Albarán {self.id_albaran} - Pedido {self.pedido.id_pedido}'


class DocumentoMercantil(models.Model):
    id_documento_mercantil = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    num_celular = models.CharField(max_length=9)
    fecha_emision = models.DateField()
    firma_recepcion = models.BooleanField()

    def __str__(self):
        return f'Documento Mercantil {self.id_documento_mercantil}'


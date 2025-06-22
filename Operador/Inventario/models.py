from django.db import models
from Cliente.producto.models import Producto

class HistorialStock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    stock_anterior = models.IntegerField()
    stock_nuevo = models.IntegerField()
    cambio = models.IntegerField()  # positivo para ingreso, negativo para salida
    motivo = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.producto.nombre_producto} - {self.fecha} ({self.cambio})"

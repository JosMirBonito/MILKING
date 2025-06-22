from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from Cliente.producto.models import Producto  # <-- Agrega esta línea


class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    nombre_cliente = models.CharField(max_length=50)
    fecha = models.DateTimeField(default=timezone.now)
    estado_envio = models.CharField(max_length=50)
    id_metodo = models.ForeignKey('MetodoPago', on_delete=models.CASCADE)
    direccion_envio = models.CharField(max_length=200, blank=True, null=True)
    telefono_envio = models.CharField(max_length=20, blank=True, null=True)
    referencia_envio = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'Pedido {self.id_pedido} - {self.nombre_cliente}'

class MetodoPago(models.Model):
    id_metodo = models.AutoField(primary_key=True)
    tipo_metodo = models.CharField(max_length=50)
    fecha = models.DateTimeField(default=timezone.now)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.tipo_metodo
    
class CarritoCompras(models.Model):
    id_carrito = models.AutoField(primary_key=True)
    nombre_cliente = models.CharField(max_length=100)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Carrito {self.id_carrito} - {self.nombre_cliente}'
    
class DetallePedido(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Detalle {self.id_detalle} Pedido {self.id_pedido.id_pedido}'
    
class ProductoCarrito(models.Model):
    id_producto_carrito = models.AutoField(primary_key=True)
    id_carrito = models.ForeignKey(CarritoCompras, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'ProductoCarrito {self.id_producto_carrito}'
    
class Pago(models.Model):
    id_pago = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.PROTECT)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50, default='Pendiente')
    referencia = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'Pago {self.id_pago} - Pedido {self.pedido.id_pedido} - {self.estado}'
from django.contrib import admin
from Cliente.producto.models import Producto, Categoria
from Cliente.pedidos.models import MetodoPago, Pedido, DetallePedido

# Registrar modelos de la app producto
admin.site.register(Producto)
admin.site.register(Categoria)

# Registrar modelos de la app pedidos
admin.site.register(MetodoPago)
admin.site.register(Pedido)
admin.site.register(DetallePedido)

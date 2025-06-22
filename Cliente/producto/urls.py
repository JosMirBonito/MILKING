from django.urls import path
from .Controller import productoController

app_name = 'producto'

urlpatterns = [
    path('', productoController.lista_productos, name='lista_productos'),
    path('categoria/<int:categoria_id>/', productoController.productos_por_categoria, name='productos_por_categoria'),
    path('carrito/agregar/<int:producto_id>/', productoController.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', productoController.ver_carrito, name='ver_carrito'),
    path('carrito/eliminar/<int:producto_carrito_id>/', productoController.eliminar_producto_carrito, name='eliminar_producto_carrito'),
]

from django.urls import path
from .Controller.DirectivoController import reporte_operaciones_inventario, reporte_productos_sin_stock, reporte_atencion_pedidos, reporte_clientes_frecuentes

urlpatterns = [
    path('reporte-operaciones/', reporte_operaciones_inventario, name='reporte_operaciones_inventario'),
    path('reporte-productos-sin-stock/', reporte_productos_sin_stock, name='reporte_productos_sin_stock'),
    path('reporte-atencion-pedidos/', reporte_atencion_pedidos, name='reporte_atencion_pedidos'),
    path('reporte-clientes-frecuentes/', reporte_clientes_frecuentes, name='reporte_clientes_frecuentes'),
]
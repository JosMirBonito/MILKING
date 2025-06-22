from django.urls import path
from .Controller import InventarioController

urlpatterns = [
    path('', InventarioController.ver_inventario, name='ver_inventario'),
    path('producto/<int:id_producto>/', InventarioController.detalle_producto, name='detalle_producto'),
    path('producto/<int:id_producto>/actualizar_precio/', InventarioController.actualizar_precio, name='actualizar_precio'),
    path('producto/<int:id_producto>/historial_stock/', InventarioController.historial_stock, name='historial_stock'),
    path('producto/<int:id_producto>/registrar_ingreso/', InventarioController.registrar_ingreso, name='registrar_ingreso'),
    path('producto/<int:id_producto>/registrar_salida/', InventarioController.registrar_salida, name='registrar_salida'),
    path('reporte/', InventarioController.reporte_inventario, name='reporte_inventario'),
]
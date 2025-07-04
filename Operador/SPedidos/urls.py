from django.urls import path
from .Controller import SpedidosController

urlpatterns = [
    path('solicitudes/', SpedidosController.ver_solicitudes_pedido, name='ver_solicitudes_pedido'),
    path('solicitud/<int:id_pedido>/', SpedidosController.ver_solicitud_pedido, name='ver_solicitud_pedido'),
    path('generar_albaran/<int:pedido_id>/', SpedidosController.generar_albaran, name='generar_albaran'),
]
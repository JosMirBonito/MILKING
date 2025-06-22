from django.urls import path
from .Controller import pedidoController

app_name = 'pedidos'  # Añadir esta línea para namespace

urlpatterns = [
    path('', pedidoController.dashboard_pedidos, name='dashboard_pedidos'),  # Dashboard con lista de pedidos
    path('nuevo/<int:producto_id>/', pedidoController.nuevo_pedido, name='nuevo_pedido'),  # Nuevo pedido con producto_id
    path('<int:id_pedido>/', pedidoController.detalle_pedido, name='detalle_pedido'),  # Detalle del pedido
    path('nuevo/', pedidoController.nuevo_pedido, name='nuevo_pedido'),
    path('confirmar_pago/<int:pedido_id>/', pedidoController.confirmar_pago, name='confirmar_pago'),

    # Nueva ruta para información de envío
    path('info_envio/<int:pedido_id>/', pedidoController.info_envio, name='info_envio'),

    # Nueva ruta para cancelar pedido
    path('cancelar/<int:pedido_id>/', pedidoController.cancelar_pedido, name='cancelar_pedido'),
]

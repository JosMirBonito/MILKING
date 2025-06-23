from django.shortcuts import render, get_object_or_404, redirect
from Cliente.pedidos.models import Pedido, DetallePedido
from ..models import Albaran

def ver_solicitudes_pedido(request):
    pedidos = Pedido.objects.all().order_by('-fecha')
    return render(request, 'SPedidos/ver_solicitudes.html', {'pedidos': pedidos})

def ver_solicitud_pedido(request, id_pedido):
    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
    if request.method == "POST" and pedido.estado_envio == "Aceptado":
        pedido.estado_envio = "En camino"
        pedido.save()
        return redirect('ver_solicitud_pedido', id_pedido=id_pedido)
    detalles = DetallePedido.objects.filter(id_pedido=pedido)
    total = sum(detalle.subtotal for detalle in detalles)
    return render(request, 'SPedidos/ver_solicitud.html', {
        'pedido': pedido,
        'detalles': detalles,
        'total': total
    })

def generar_albaran(request, pedido_id):
    pedido = get_object_or_404(Pedido, id_pedido=pedido_id)
    if request.method == "POST":
        pedido.estado_envio = "Entregado"
        pedido.save()
        Albaran.objects.get_or_create(pedido=pedido)
        return redirect('pedidos:detalle_pedido', id_pedido=pedido.id_pedido)
    return redirect('ver_solicitud_pedido', id_pedido=pedido_id)

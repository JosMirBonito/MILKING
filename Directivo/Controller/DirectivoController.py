from django.shortcuts import render
from Operador.Inventario.models import HistorialStock  # Importa el modelo de historial
from Cliente.producto.models import Producto
from Cliente.pedidos.models import Pedido, MetodoPago
from django.db.models import Count

def vista_directivo(request):
    return render(request, 'reporte/vista_directivo.html')

def reporte_operaciones_inventario(request):
    historial = HistorialStock.objects.select_related('producto').order_by('-fecha')
    return render(request, 'reporte/reporte_operaciones_inventario.html', {'historial': historial})

def reporte_productos_sin_stock(request):
    productos_sin_stock = Producto.objects.filter(stock=0)
    return render(request, 'reporte/reporte_productos_sin_stock.html', {'productos': productos_sin_stock})

def reporte_atencion_pedidos(request):
    pedidos = Pedido.objects.select_related('id_metodo').order_by('-fecha')
    return render(request, 'reporte/reporte_atencion_pedidos.html', {'pedidos': pedidos})

def reporte_clientes_frecuentes(request):
    clientes = (
        Pedido.objects.values('nombre_cliente')
        .annotate(total_pedidos=Count('id_pedido'))
        .order_by('-total_pedidos')
    )
    return render(request, 'reporte/reporte_clientes_frecuentes.html', {'clientes': clientes})

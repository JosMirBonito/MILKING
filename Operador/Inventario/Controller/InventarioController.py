from django.shortcuts import render, redirect, get_object_or_404
from Cliente.producto.models import Producto
from django.contrib import messages
from Operador.Inventario.models import HistorialStock

def ver_inventario(request):
    productos = Producto.objects.all()
    return render(request, 'inventario/ver_inventario.html', {'productos': productos})

def detalle_producto(request, id_producto):
    producto = get_object_or_404(Producto, id_producto=id_producto)
    return render(request, 'inventario/detalle_producto.html', {'producto': producto})

def actualizar_precio(request, id_producto):
    producto = get_object_or_404(Producto, id_producto=id_producto)
    if request.method == 'POST':
        nuevo_precio = request.POST.get('precio')
        if nuevo_precio:
            producto.precio = nuevo_precio
            producto.save()
            messages.success(request, 'Precio actualizado correctamente.')
            return redirect('detalle_producto', id_producto=producto.id_producto)
    return render(request, 'inventario/actualizar_precio.html', {'producto': producto})

def historial_stock(request, id_producto):
    producto = get_object_or_404(Producto, id_producto=id_producto)
    historial = HistorialStock.objects.filter(producto=producto).order_by('-fecha')
    return render(request, 'inventario/historial_stock.html', {'producto': producto, 'historial': historial})

def registrar_ingreso(request, id_producto):
    producto = get_object_or_404(Producto, id_producto=id_producto)
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 0))
        if cantidad > 0:
            stock_anterior = producto.stock
            producto.stock += cantidad
            producto.save()
            HistorialStock.objects.create(
                producto=producto,
                stock_anterior=stock_anterior,
                stock_nuevo=producto.stock,
                cambio=cantidad,
                motivo="Ingreso de producto"
            )
            messages.success(request, 'Ingreso registrado correctamente.')
            return redirect('detalle_producto', id_producto=producto.id_producto)
    return render(request, 'inventario/registrar_ingreso.html', {'producto': producto})

def registrar_salida(request, id_producto):
    producto = get_object_or_404(Producto, id_producto=id_producto)
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 0))
        if 0 < cantidad <= producto.stock:
            stock_anterior = producto.stock
            producto.stock -= cantidad
            producto.save()
            HistorialStock.objects.create(
                producto=producto,
                stock_anterior=stock_anterior,
                stock_nuevo=producto.stock,
                cambio=-cantidad,
                motivo="Salida de producto"
            )
            messages.success(request, 'Salida registrada correctamente.')
            return redirect('detalle_producto', id_producto=producto.id_producto)
    return render(request, 'inventario/registrar_salida.html', {'producto': producto})

def reporte_inventario(request):
    productos = Producto.objects.all()
    return render(request, 'inventario/reporte_inventario.html', {'productos': productos})
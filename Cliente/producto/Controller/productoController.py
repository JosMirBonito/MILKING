from django.shortcuts import redirect, render, get_object_or_404
from ..models import Producto, Categoria  # Modelos de la app producto
from Cliente.pedidos.models import CarritoCompras, ProductoCarrito  # Modelos de la app pedidos
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from ..forms import AgregarCantidadForm


def lista_productos(request):
    categorias = Categoria.objects.all()
    productos = Producto.objects.filter(stock__gt=0)
    context = {
        'categorias': categorias,
        'productos': productos,
        'categoria_actual': None,  # Indica que estamos en "Todas"
    }
    return render(request, 'producto/lista_productos.html', context)




@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)
    cliente = request.user.cliente

    if request.method == 'POST':
        try:
            cantidad = int(request.POST.get('cantidad', 0))
        except (TypeError, ValueError):
            cantidad = 0

        if cantidad < 1 or cantidad > producto.stock:
            messages.error(request, f"La cantidad debe ser entre 1 y {producto.stock}.")
            return redirect('producto:lista_productos')

        carrito, creado = CarritoCompras.objects.get_or_create(
            nombre_cliente=cliente.nombre_cliente,
            defaults={'total': 0}
        )

        prod_carrito, creado = ProductoCarrito.objects.get_or_create(
            id_carrito=carrito,
            id_producto=producto,
            defaults={'cantidad': cantidad, 'subtotal': producto.precio * cantidad}
        )
        if not creado:
            prod_carrito.cantidad += cantidad
            prod_carrito.subtotal = prod_carrito.cantidad * producto.precio
            prod_carrito.save()

        # Actualizar total carrito
        productos_carrito = ProductoCarrito.objects.filter(id_carrito=carrito)
        total = sum(p.subtotal for p in productos_carrito)
        carrito.total = total
        carrito.save()

        messages.success(request, f'Producto "{producto.nombre_producto}" añadido al carrito.')
        return redirect('producto:lista_productos')
    else:
        return redirect('producto:lista_productos')
    
   
@login_required
def ver_carrito(request):
    cliente = request.user.cliente
    carrito = CarritoCompras.objects.filter(nombre_cliente=cliente.nombre_cliente).first()
    productos = []
    if carrito:
        productos = ProductoCarrito.objects.filter(id_carrito=carrito)

    return render(request, 'producto/carrito.html', {'carrito': carrito, 'productos': productos})

@login_required
def eliminar_producto_carrito(request, producto_carrito_id):
    item = get_object_or_404(ProductoCarrito, id_producto_carrito=producto_carrito_id)
    carrito = item.id_carrito  # Guarda referencia al carrito antes de borrar
    item.delete()
    # Recalcula el total del carrito
    productos_carrito = ProductoCarrito.objects.filter(id_carrito=carrito)
    total = sum(p.subtotal for p in productos_carrito)
    carrito.total = total
    carrito.save()
    return redirect('producto:ver_carrito')

@login_required
def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id_categoria=categoria_id)
    productos = Producto.objects.filter(id_categoria=categoria, stock__gt=0)
    categorias = Categoria.objects.all()
    context = {
        'productos': productos,
        'categorias': categorias,
        'categoria_actual': categoria
    }
    return render(request, 'producto/lista_productos.html', context)

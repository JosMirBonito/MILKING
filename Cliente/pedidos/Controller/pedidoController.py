from django.shortcuts import render, redirect
from ..forms import PedidoForm, PagoForm, EnvioForm , ConformidadForm
from django.contrib.auth.decorators import login_required
from ..models import Pedido, CarritoCompras, ProductoCarrito, DetallePedido, Pago, MetodoPago, DocumentoConformidad
from django.shortcuts import get_object_or_404
from django.contrib import messages 
from django.utils import timezone


def dashboard_pedidos(request):
    usuario = request.user
    cliente = usuario.cliente
    # Obtener pedidos ordenados por fecha y enumerar desde 1
    pedidos = Pedido.objects.filter(
        nombre_cliente=cliente.nombre_cliente
    ).order_by('fecha')
    
    # Crear una lista de pedidos con números secuenciales
    pedidos_enumerados = []
    for index, pedido in enumerate(pedidos, 1):
        pedido.numero_visual = index  # Agrega un número secuencial al pedido
        pedidos_enumerados.append(pedido)
    
    return render(request, 'pedidos/dashboard.html', {
        'pedidos': pedidos_enumerados
    })


@login_required
def nuevo_pedido(request):
    cliente = request.user.cliente
    carrito = CarritoCompras.objects.filter(nombre_cliente=cliente.nombre_cliente).first()
    if not carrito:
        messages.error(request, "Tu carrito está vacío.")
        return redirect('lista_productos')

    if request.method == 'POST':
        metodo_pago = MetodoPago.objects.first()  # Usa el primer método de pago disponible
        if not metodo_pago:
            messages.error(request, "No hay métodos de pago configurados.")
            return redirect('lista_productos')

        pedido = Pedido.objects.create(
            nombre_cliente=cliente.nombre_cliente,
            fecha=timezone.now(),
            estado_envio='Pendiente',  # O el valor que corresponda
            id_metodo=metodo_pago
        )

        # Guardar detalles del pedido
        for producto_carrito in ProductoCarrito.objects.filter(id_carrito=carrito):
            DetallePedido.objects.create(
                id_pedido=pedido,
                id_producto=producto_carrito.id_producto,
                cantidad=producto_carrito.cantidad,
                precio=producto_carrito.id_producto.precio,
                subtotal=producto_carrito.subtotal
            )

        carrito.delete()
        messages.success(request, "Pedido creado correctamente.")
        return redirect('pedidos:info_envio', pedido_id=pedido.id_pedido)
    else:
        return redirect('lista_productos')



def detalle_pedido(request, id_pedido):
    usuario = request.user
    cliente = usuario.cliente
    pedidos = Pedido.objects.filter(nombre_cliente=cliente.nombre_cliente).order_by('fecha')
    pedidos_enumerados = []
    numero_visual = None
    for index, pedido in enumerate(pedidos, 1):
        if pedido.id_pedido == int(id_pedido):
            numero_visual = index
        pedidos_enumerados.append(pedido)
    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
    detalles = pedido.detallepedido_set.all()
    total = sum(detalle.subtotal for detalle in detalles)
    return render(request, 'pedidos/detalle_pedido.html', {
        'pedido': pedido,
        'detalles': detalles,
        'numero_visual': numero_visual,
        'total': total
    })

@login_required
def confirmar_pago(request, pedido_id):
    pedido = get_object_or_404(Pedido, id_pedido=pedido_id, nombre_cliente=request.user.cliente.nombre_cliente)

    # Calcula el total sumando los subtotales de los detalles
    detalles = pedido.detallepedido_set.all()
    total = sum(d.subtotal for d in detalles)

    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            metodo_pago = form.cleaned_data['metodo_pago']
            monto = total  # Usa el total calculado

            # Cuando el pago se confirma exitosamente
            pago = Pago.objects.create(
                pedido=pedido,
                metodo_pago=metodo_pago,
                monto=monto,
                estado='Pagado',
            )
            pedido.estado_envio = 'Registrado'
            pedido.save()

            messages.success(request, "Pago registrado correctamente.")
            return redirect('pedidos:dashboard_pedidos')
    else:
        form = PagoForm()

    return render(request, 'pedidos/confirmar_pago.html', {'form': form, 'pedido': pedido, 'total': total})

@login_required
def info_envio(request, pedido_id):
    pedido = get_object_or_404(Pedido, id_pedido=pedido_id, nombre_cliente=request.user.cliente.nombre_cliente)
    if request.method == 'POST':
        form = EnvioForm(request.POST)
        if form.is_valid():
            pedido.direccion_envio = form.cleaned_data['direccion']
            pedido.telefono_envio = form.cleaned_data['telefono']
            pedido.referencia_envio = form.cleaned_data['referencia']
            pedido.save()
            return redirect('pedidos:confirmar_pago', pedido_id=pedido.id_pedido)
    else:
        form = EnvioForm()
    return render(request, 'pedidos/info_envio.html', {'form': form, 'pedido': pedido})

@login_required
def cancelar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id_pedido=pedido_id, nombre_cliente=request.user.cliente.nombre_cliente)
    if pedido.estado_envio == 'Registrado' and request.method == 'POST':
        pedido.delete()
        messages.success(request, "Pedido cancelado exitosamente.")
    return redirect('pedidos:dashboard_pedidos')


def registrar_conformidad(request, pedido_id):
    pedido = get_object_or_404(Pedido, id_pedido=pedido_id)
    if request.method == "POST":
        form = ConformidadForm(request.POST)
        if form.is_valid():
            # Cambia el estado del pedido
            pedido.estado_envio = "Entregado"
            pedido.save()
            # Guarda el documento de conformidad
            DocumentoConformidad.objects.create(
                id_pedido=pedido,
                fecha_recepcion=timezone.now().date(),
                nombre_receptor=request.user.get_full_name() or request.user.username,
                firma_receptor=form.cleaned_data['conforme'],
                fecha_conformidad=timezone.now().date(),
                # Si tienes el campo comentario en el form:
                # comentario=form.cleaned_data.get('comentario', '')
            )
            return render(request, 'pedidos/gracias.html')
    else:
        form = ConformidadForm()
    return render(request, 'pedidos/registrar_conformidad.html', {'form': form, 'pedido': pedido})
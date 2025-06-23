from django import forms
from .models import Pedido, MetodoPago  # Cambiado para importar desde pedidos.models

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['nombre_cliente', 'fecha', 'estado_envio', 'id_metodo']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

class PagoForm(forms.Form):
    metodo_pago = forms.ModelChoiceField(
        queryset=MetodoPago.objects.all(), 
        empty_label="Seleccione método de pago"
    )

class EnvioForm(forms.Form):
    direccion = forms.CharField(max_length=200, label="Dirección de envío")
    telefono = forms.CharField(max_length=20, label="Teléfono de contacto")
    referencia = forms.CharField(max_length=200, label="Referencia", required=False)


class ConformidadForm(forms.Form):
    conforme = forms.BooleanField(label="¿Está conforme con su pedido?", required=True)
    comentario = forms.CharField(label="Comentario", required=False, widget=forms.Textarea)
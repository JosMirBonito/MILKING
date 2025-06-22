from django import forms

class AgregarCantidadForm(forms.Form):
    cantidad = forms.IntegerField(min_value=1, label="Cantidad")

    def __init__(self, max_stock=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if max_stock is not None:
            self.fields['cantidad'].max_value = max_stock
            self.fields['cantidad'].widget.attrs.update({'max': max_stock})


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from gestion import models
from django.forms import inlineformset_factory, modelformset_factory, formset_factory


class RegistroForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class OrdenCompraForm(forms.ModelForm):
    class Meta:
        model = models.OrdenCompra
        fields = '__all__'

class ItemOrdenForm(forms.ModelForm):
    class Meta:
        model = models.ItemOrden
        fields = ['producto', 'cantidad', 'prioridad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'prioridad': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ModificarPrioridadForm(forms.Form):
    def __init__(self, items_orden, *args, **kwargs):
        super(ModificarPrioridadForm, self).__init__(*args, **kwargs)

        # Agregar un campo de prioridad para cada elemento en items_orden
        for item in items_orden:
            field_name = f'prioridad_{item.pk}'
            self.fields[field_name] = forms.BooleanField(label=str(item), required=False)

class DespachoForm(forms.Form):
    opciones_despacho = [
        ('camion', 'Camión'),
        ('rampla', 'Rampla'),
    ]
    opcion_despacho = forms.ChoiceField(choices=opciones_despacho, label='Seleccione una opción de despacho')

class StockForm(forms.ModelForm):
    # Cambia el nombre del campo 'cantidad_en_stock' a 'cantidad_despachada'
    cantidad_despachada = forms.IntegerField(label='Cantidad despachada', widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = models.Producto
        fields = ['nombre', 'cantidad_despachada']  # Actualiza el nombre del campo aquí también
        widgets = {
            'nombre': forms.Select(attrs={'class': 'form-control'}),
        }

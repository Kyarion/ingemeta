from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from gestion import forms
from gestion import models
from django.forms import formset_factory
from django.utils import timezone


# Create your views here.

def home(request):
    return render(request, 'home.html')

def registro_usuario(request):
    if request.method == 'POST':
        form = forms.RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Cambia 'home' con el nombre de tu vista de inicio
    else:
        form = forms.RegistroForm()

    return render(request, 'registro.html', {'form': form})

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form' : AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form' : AuthenticationForm,
                'error': 'El usuario o la contraseña esta incorrecta'
            })
        else:
            login(request, user)
            return redirect('home')

def signout(request):
    logout(request)
    return redirect('home')

def crear_orden_compra(request):
    ItemOrdenFormSet = formset_factory(forms.ItemOrdenForm)

    if request.method == 'POST':
        orden_form = forms.OrdenCompraForm(request.POST)
        item_formset = ItemOrdenFormSet(request.POST)

        if orden_form.is_valid() and item_formset.is_valid():
            orden = orden_form.save()
            for form in item_formset:
                item_orden = form.save(commit=False)
                item_orden.orden_compra = orden
                item_orden.save()
            return redirect('detalle_orden_compra', pk=orden.pk)
    else:
        orden_form = forms.OrdenCompraForm()
        item_formset = ItemOrdenFormSet()

    return render(request, 'crear_orden_compra.html', {'orden_form': orden_form, 'item_formset': item_formset})
    
    
def detalle_orden_compra(request, pk):
    orden_compra = get_object_or_404(models.OrdenCompra, pk=pk)
    productos_pilares_cadenas = models.Producto.objects.filter(codigo_producto__in=['pilares', 'cadenas']) 
    # Verificar si los productos 'pilares' y 'cadenas' están en el modelo OrdenProduccion 
    for producto in productos_pilares_cadenas: 
        if not models.OrdenProduccion.objects.filter(producto=producto).exists(): 
            models.OrdenProduccion.objects.create(producto=producto, cantidad=0, numero_secuencia=1) 
        # Actualizamos los valores de cantidad segun ItemOrden 
        productos_orden = models.ItemOrden.objects.filter(revisado=False) 
        for producto in productos_orden: 
            producto_seleccionado = get_object_or_404(models.OrdenProduccion, producto=producto.producto) 
            producto_seleccionado.cantidad += producto.cantidad 
            producto.revisado = True 
            producto.save() 
            producto_seleccionado.save() 
    return render(request, 'detalle_orden_compra.html', {'orden_compra': orden_compra})

def modificar_prioridad(request, pk):
    orden_compra = models.OrdenCompra.objects.get(pk=pk)
    items_orden = orden_compra.items.all()

    if request.method == 'POST':
        form = forms.ModificarPrioridadForm(items_orden, request.POST)
        if form.is_valid():
            for item in items_orden:
                prioridad_key = f'prioridad_{item.pk}'
                if prioridad_key in form.cleaned_data:
                    item.prioridad = form.cleaned_data[prioridad_key]
                    item.save()
    else:
        # Obtén los valores iniciales de los campos de prioridad
        initial_data = {}
        for item in items_orden:
            prioridad_key = f'prioridad_{item.pk}'
            initial_data[prioridad_key] = item.prioridad
        form = forms.ModificarPrioridadForm(items_orden=items_orden, initial=initial_data)

    return render(request, 'modificar_prioridad.html', {'form': form, 'orden_compra': orden_compra})
    
def lista_ordenes_compra(request):
    ordenes_compra = models.OrdenCompra.objects.order_by('-fecha_emision')
    return render(request, 'lista_ordenes_compra.html', {'ordenes_compra': ordenes_compra})

def produccion(request):
    return render(request, 'produccion.html')
        
def fin_produccion(request):
    produccion_en_curso = models.Produccion.objects.filter(en_curso=True).last()
    StockFormSet = formset_factory(forms.CambioStockForm)

    if request.method == 'POST':
        #POST para cambio de rollo
        if produccion_en_curso.tipo == 'cambio_rollo':
            produccion_en_curso.hora_termino = timezone.now()
            produccion_en_curso.en_curso = False
            producto_id = request.POST.get('producto_rollo')
            producto_seleccionado = get_object_or_404(models.Producto, pk=producto_id)
            producto_seleccionado.cantidad_en_stock -= 1
            producto_seleccionado.save()
        #POST para despacho
        elif produccion_en_curso.tipo == 'despacho':
            produccion_en_curso.hora_termino = timezone.now()
            produccion_en_curso.en_curso = False
            form_despacho = forms.DespachoForm(request.POST)
            item_formset = StockFormSet(request.POST)
            if form_despacho.is_valid() and item_formset.is_valid():
                produccion_en_curso.nota = form_despacho.cleaned_data['opcion_despacho']
                for form in item_formset:
                    # Obtener los datos de cada formulario en el formset
                    producto = form.cleaned_data['producto']
                    cantidad = form.cleaned_data['cantidad']

                    # Obtener el producto seleccionado
                    producto_seleccionado = get_object_or_404(models.Producto, pk=producto.pk)

                    # Actualizar la cantidad de stock del producto
                    producto_seleccionado.cantidad_en_stock -= cantidad
                    producto_seleccionado.save()
        #POST para ingreso de material
        elif produccion_en_curso.tipo == 'ingreso_material':
            produccion_en_curso.hora_termino = timezone.now()
            produccion_en_curso.en_curso = False
            material_ingreso = models.Producto.objects.filter(codigo_producto='rollos')
            for material in material_ingreso:
                cantidad = int(request.POST.get(f'cantidad_{material.id}', 0))
                material.cantidad_en_stock += cantidad
                material.save()
        #POST para Setup o Ajustes
        elif produccion_en_curso.tipo == 'setup_ajustes':
            produccion_en_curso.hora_termino = timezone.now()
            produccion_en_curso.en_curso = False
            producto_id = request.POST.get('material_ajuste')
            if producto_id:
                producto_seleccionado = get_object_or_404(models.Producto, pk=producto_id)
                produccion_en_curso.nota = producto_seleccionado.nombre
                produccion_en_curso.save()
        #POST para Pana o Mantencion
        elif  produccion_en_curso.tipo == 'pana_mantencion':
            produccion_en_curso.hora_termino = timezone.now()
            produccion_en_curso.en_curso = False
            produccion_en_curso.nota = request.POST.get('observaciones')
        #POST para Produccion
        elif produccion_en_curso.tipo == 'produccion':
            produccion_en_curso.hora_termino = timezone.now()
            produccion_en_curso.en_curso = False
            producto_id = request.POST.get('produccion_actual')
            cantid = request.POST.get('cantidad')
            if producto_id and cantid:
                producto_seleccionado = get_object_or_404(models.Producto, pk=producto_id)
                producto_seleccionado2 = get_object_or_404(models.OrdenProduccion, pk=producto_id)
                producto_seleccionado.cantidad_en_stock += int(cantid)
                producto_seleccionado2.cantidad -= int(cantid)
                producto_seleccionado2.save()
                producto_seleccionado.save()
        produccion_en_curso.save()
        return redirect('produccion')
    else:
        if produccion_en_curso.tipo == 'cambio_rollo':
            productos_rollo = models.Producto.objects.filter(codigo_producto='rollos')
            return render(request, 'fin_produccion.html', {'produccion_en_curso': produccion_en_curso, 'productos_rollo': productos_rollo})
        elif produccion_en_curso.tipo == 'despacho':
            form_despacho = forms.DespachoForm()
            item_formset = StockFormSet()
            return render(request, 'fin_produccion.html', {'produccion_en_curso': produccion_en_curso, 'form_despacho': form_despacho, 'item_formset': item_formset})
        elif produccion_en_curso.tipo == 'ingreso_material':
            material_ingreso = models.Producto.objects.filter(codigo_producto='rollos')
            item_formset = StockFormSet()
            return render(request, 'fin_produccion.html', {'produccion_en_curso': produccion_en_curso, 'material_ingreso': material_ingreso, 'item_formset': item_formset})
        elif produccion_en_curso.tipo == 'setup_ajustes':
            ajustes = models.Producto.objects.filter(codigo_producto__in=['cadenas', 'pilares'])
            return render(request, 'fin_produccion.html', {'produccion_en_curso': produccion_en_curso, 'ajustes': ajustes})
        elif produccion_en_curso.tipo == 'pana_mantencion':
            return render(request, 'fin_produccion.html', {'produccion_en_curso': produccion_en_curso})
        elif produccion_en_curso.tipo == 'produccion':
            productos = models.Producto.objects.filter(codigo_producto__in=['cadenas', 'pilares'])
            return render(request, 'fin_produccion.html', {'produccion_en_curso': produccion_en_curso, 'productos': productos})

def cambio_rollo(request):
    if models.Produccion.objects.filter(en_curso=True).exists():
        # Si hay una producción en curso, redirigir a la página de fin_cambio_rollo
        return redirect('fin_produccion')
    else:
        # Si no hay una producción en curso, crear una nueva
        produccion = models.Produccion.objects.create(
            tipo='cambio_rollo',
            hora_inicio=timezone.now(),
            hora_termino=timezone.now()  # Se actualiza automáticamente al guardar
        )
        return redirect('fin_produccion')
    
def despacho(request):
    if models.Produccion.objects.filter(en_curso=True).exists():
        # Si hay una producción en curso, redirigir a la página de fin_cambio_rollo
        return redirect('fin_produccion')
    else:
        # Si no hay una producción en curso, crear una nueva
        produccion = models.Produccion.objects.create(
            tipo='despacho',
            hora_inicio=timezone.now(),
            hora_termino=timezone.now()  # Se actualiza automáticamente al guardar
        )
        return redirect('fin_produccion')

def ingreso_material(request):
    if models.Produccion.objects.filter(en_curso=True).exists():
        # Si hay una producción en curso, redirigir a la página de fin_cambio_rollo
        return redirect('fin_produccion')
    else:
        # Si no hay una producción en curso, crear una nueva
        produccion = models.Produccion.objects.create(
            tipo='ingreso_material',
            hora_inicio=timezone.now(),
            hora_termino=timezone.now()  # Se actualiza automáticamente al guardar
        )
        return redirect('fin_produccion')

def setup_ajustes(request):
    if models.Produccion.objects.filter(en_curso=True).exists():
        # Si hay una producción en curso, redirigir a la página de fin_cambio_rollo
        return redirect('fin_produccion')
    else:
        # Si no hay una producción en curso, crear una nueva
        produccion = models.Produccion.objects.create(
            tipo='setup_ajustes',
            hora_inicio=timezone.now(),
            hora_termino=timezone.now()  # Se actualiza automáticamente al guardar
        )
        return redirect('fin_produccion')

def pana_mantencion(request):
    if models.Produccion.objects.filter(en_curso=True).exists():
        # Si hay una producción en curso, redirigir a la página de fin_cambio_rollo
        return redirect('fin_produccion')
    else:
        # Si no hay una producción en curso, crear una nueva
        produccion = models.Produccion.objects.create(
            tipo='pana_mantencion',
            hora_inicio=timezone.now(),
            hora_termino=timezone.now()  # Se actualiza automáticamente al guardar
        )
        return redirect('fin_produccion')

def produccion_iniciar(request):
    if models.Produccion.objects.filter(en_curso=True).exists():
        # Si hay una producción en curso, redirigir a la página de fin_cambio_rollo
        return redirect('fin_produccion')
    else:
        # Si no hay una producción en curso, crear una nueva
        produccion = models.Produccion.objects.create(
            tipo='produccion',
            hora_inicio=timezone.now(),
            hora_termino=timezone.now()  # Se actualiza automáticamente al guardar
        )
        return redirect('fin_produccion')
    
def orden_produccion(request):
    if request.method == 'POST':
            return HttpResponse("Formulario inválido")
    else:
        orden_produccion_queryset = models.OrdenProduccion.objects.order_by('numero_secuencia', '-cantidad')
        return render(request, 'orden_produccion.html', {'orden_produccion_queryset': orden_produccion_queryset})

def modificar_orden_produccion(request):
    if request.method == 'POST':
        # Procesar la actualización de las prioridades
        for orden_id, nueva_prioridad in request.POST.items():
            if orden_id.startswith('prioridad_'):
                orden_id = orden_id.split('_')[1]
                try:
                    orden = models.OrdenProduccion.objects.get(pk=orden_id)
                    orden.numero_secuencia = int(nueva_prioridad)
                    orden.save()
                except models.OrdenProduccion.DoesNotExist:
                    return HttpResponse('Orden de Producción no encontrada', status=404)
        return redirect('orden_produccion')

    # Solicitud GET, mostrar la lista de órdenes de producción con cantidad > 0
    ordenes_produccion = models.OrdenProduccion.objects.filter(cantidad__gt=0).order_by('numero_secuencia')
    context = {
        'ordenes_produccion': ordenes_produccion
    }
    return render(request, 'modificar_orden_produccion.html', context)
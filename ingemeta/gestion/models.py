from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
"""
class PosiblesCargasCamion(models.Model):
    medida_cargas = models.FloatField(decimal_places=2)

class CargasCamion(models.Model):
    medida_cargas = models.FloatField(decimal_places=2)
"""

class Stock(models.Model):
    nombre_stock = models.CharField(max_length=30)
    cantidad_stock = models.IntegerField()

class ProduccionIdeal(models.Model):
    nombre_produccion = models.CharField(max_length=30)
    produccionideal = models.IntegerField()

class Produccion(models.Model):
    TIPOS_CHOICES = [
        ('cambio_rollo', 'Cambio de Rollo'),
        ('despacho', 'Despacho'),
        ('ingreso_material', 'Ingreso de Material'),
        ('pana_mantencion', 'Pana o Mantención'),
        ('produccion', 'Producción'),
        ('setup_ajustes', 'Setup o Ajustes'),
    ]

    nombre_producto = models.CharField(max_length=30)
    fecha_pedido = models.DateField(auto_now_add=True)
    hora_inicio = models.TimeField()
    hora_termino = models.TimeField()
    tipo = models.CharField(max_length=30, choices=TIPOS_CHOICES)
    cantidad = models.IntegerField(default=0)
    nota = models.TextField(blank=True)
    en_curso = models.BooleanField(default=False)  # Flag para indicar si la producción está en curso
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.pk:  # Si es una nueva instancia
            self.en_curso = True  # Marcar la producción como en curso al ser creada
        super(Produccion, self).save(*args, **kwargs)

class Producto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    precio = models.IntegerField()
    cantidad_en_stock = models.IntegerField(default=0)
    codigo_producto = models.CharField(max_length=50)
    fecha_modificacion = models.DateField(auto_now=True)
    ancho = models.IntegerField(default=0)
    alto = models.IntegerField(default=0)
    largo = models.FloatField(default=0)
    diametro = models.FloatField(default=0)
    peso = models.FloatField(default=0)

    def __str__(self):
        return self.nombre

class OrdenCompra(models.Model):
    numero_orden = models.CharField(max_length=100, unique=True)
    fecha_emision = models.DateField(auto_now_add=True)
    fecha_entrega_esperada = models.DateField()
    total_orden = models.IntegerField()
    ESTADOS_ORDEN = [
        ('PROCESO', 'En proceso'),
        ('COMPLETADA', 'Completada'),
        ('CANCELADA', 'Cancelada'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADOS_ORDEN, default='PROCESO')

class ItemOrden(models.Model):
    orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    cantidad_producida = models.IntegerField(default=0)
    prioridad = models.BooleanField(default=False)
    revisado = models.BooleanField(default=False)

class CambioStock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

class OrdenProduccion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    numero_secuencia = models.IntegerField(default=0)

    class Meta:
        ordering = ['numero_secuencia', '-cantidad']  # Ordena por cantidad de forma predeterminada

# orden_produccion_queryset = OrdenProduccion.objects.order_by('numero_secuencia') usar este codigo para el orden manual
# orden_produccion_queryset = OrdenProduccion.objects.all() usar este codigo para el orden por cantidad



from django.db import models

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
    nombre_producto = models.CharField(max_length=30)
    fecha_pedido = models.DateField(auto_now_add=True)
    hora_inicio = models.TimeField()
    hora_termino = models.TimeField()
    tipo = models.CharField(max_length=30)
    cantidad = models.IntegerField(default=0)
    duracion_produccion = models.DurationField(null=True, blank=True)
    produccion_por_hora = models.FloatField(null=True, blank=True)
    nota = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # Calcular la diferencia entre la hora de inicio y la de término
        if self.hora_inicio and self.hora_termino:
            diferencia = self.hora_termino - self.hora_inicio
            self.duracion_produccion = diferencia

            # Calcular la producción por hora
            if diferencia.total_seconds() > 0:
                produccion_por_hora = self.cantidad / (diferencia.total_seconds() / 3600)
                self.produccion_por_hora = round(produccion_por_hora, 2)

class Pedidos(models.Model):
    id_pedido = models.IntegerField()
    nombre_pedido = models.CharField(max_length=30)
    cantidad = models.IntegerField()
# Generated by Django 4.2.4 on 2024-01-24 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pedidos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_pedido', models.IntegerField()),
                ('nombre_pedido', models.CharField(max_length=30)),
                ('cantidad', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Produccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_producto', models.CharField(max_length=30)),
                ('fecha_pedido', models.DateField(auto_now_add=True)),
                ('hora_inicio', models.TimeField()),
                ('hora_termino', models.TimeField()),
                ('tipo', models.CharField(max_length=30)),
                ('cantidad', models.IntegerField(default=0)),
                ('duracion_produccion', models.DurationField(blank=True, null=True)),
                ('produccion_por_hora', models.FloatField(blank=True, null=True)),
                ('nota', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProduccionIdeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_produccion', models.CharField(max_length=30)),
                ('produccionideal', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_stock', models.CharField(max_length=30)),
                ('cantidad_stock', models.IntegerField()),
            ],
        ),
    ]

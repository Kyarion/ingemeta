# Generated by Django 4.2.4 on 2024-01-25 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0004_itemorden_prioridad'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordencompra',
            name='cliente',
        ),
        migrations.RemoveField(
            model_name='ordencompra',
            name='direccion_envio',
        ),
        migrations.RemoveField(
            model_name='ordencompra',
            name='direccion_facturacion',
        ),
        migrations.RemoveField(
            model_name='ordencompra',
            name='informacion_pago',
        ),
        migrations.RemoveField(
            model_name='ordencompra',
            name='metodo_envio',
        ),
        migrations.RemoveField(
            model_name='ordencompra',
            name='notas',
        ),
        migrations.AlterField(
            model_name='ordencompra',
            name='estado',
            field=models.CharField(choices=[('PROCESO', 'En proceso'), ('COMPLETADA', 'Completada'), ('CANCELADA', 'Cancelada')], default='PROCESO', max_length=20),
        ),
        migrations.AlterField(
            model_name='ordencompra',
            name='total_orden',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio',
            field=models.IntegerField(),
        ),
    ]

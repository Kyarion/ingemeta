# Generated by Django 4.2.4 on 2024-02-19 16:10

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0011_alter_produccion_hora_inicio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produccion',
            name='hora_inicio',
            field=models.TimeField(verbose_name=datetime.datetime(2024, 2, 19, 16, 10, 27, 54683)),
        ),
        migrations.AlterField(
            model_name='produccion',
            name='hora_termino',
            field=models.TimeField(verbose_name=datetime.datetime(2024, 2, 19, 16, 10, 27, 54683)),
        ),
        migrations.CreateModel(
            name='CambioStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.producto')),
            ],
        ),
    ]

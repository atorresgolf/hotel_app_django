# Generated by Django 4.1.3 on 2022-12-10 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaHabitacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True)),
                ('descripcion', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'categoria',
            },
        ),
        migrations.CreateModel(
            name='Habitacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField(max_length=3, unique=True)),
                ('piso', models.IntegerField(max_length=2, unique=True)),
                ('camas', models.IntegerField(default=1)),
                ('capacidad', models.IntegerField(blank=True, max_length=1, null=True)),
                ('precio', models.FloatField(blank=True, max_length=7, null=True)),
                ('detalle', models.CharField(blank=True, max_length=150, null=True)),
                ('estado', models.IntegerField(default=1, help_text='Ocupada 0, Desocupada 1, Mantenimiento 2')),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appstaff.categoriahabitacion')),
            ],
            options={
                'db_table': 'room',
            },
        ),
    ]

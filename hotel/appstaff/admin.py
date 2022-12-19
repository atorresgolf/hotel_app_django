from django.contrib import admin
from .models import CategoriaHabitacion, Habitacion, Reserva
# Register your models here.
admin.site.register(CategoriaHabitacion)
admin.site.register(Habitacion)
admin.site.register(Reserva)
from django.db import models
from django.contrib.auth.models import User
# mypaymentapp/models.py
from decimal import Decimal

'''from payments import PurchasedItem
from payments.models import BasePayment

class Payment(BasePayment):

    def get_failure_url(self) -> str:
        # Return a URL where users are redirected after
        # they fail to complete a payment:
        return f"http://example.com/payments/{self.pk}/failure"

    def get_success_url(self) -> str:
        # Return a URL where users are redirected after
        # they successfully complete a payment:
        return f"http://example.com/payments/{self.pk}/success"

    def get_purchased_items(self) -> Iterable[PurchasedItem]:
        # Return items that will be included in this payment.
        yield PurchasedItem(
            name='The Hound of the Baskervilles',
            sku='BSKV',
            quantity=9,
            price=Decimal(10),
            currency='USD',
        )'''
# Create your models here.
class CategoriaHabitacion(models.Model):
    class Meta:
        db_table = 'categoria_habitacion'
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.nombre}'   

class Habitacion(models.Model):
    class Meta:
        db_table = 'habitacion'
    numero =  models.IntegerField( unique = True)
    piso = models.IntegerField(blank=True , null= True)
    camas = models.IntegerField(default=1)
    capacidad = models.IntegerField(blank=True , null= True)
    precio = models.FloatField(max_length=7, blank=True , null= True)
    detalle = models.CharField(max_length=150, blank=True , null= True)
    estado = models.IntegerField(default=1, help_text= 'Ocupada 0, Desocupada 1, Mantenimiento 2')
    categoria = models.ForeignKey(CategoriaHabitacion,  on_delete=models.CASCADE, blank=True , null= True)

    def __str__(self):
        return f'{self.numero}. Camas = {self.camas} Capacidad = {self.capacidad}'   

class Reserva(models.Model):
    class Meta:
        db_table = 'reservas'
        get_latest_by = ['id']
    room = models.ForeignKey(Habitacion, on_delete=models.CASCADE, default=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)
    adultos = models.IntegerField(null=True, blank=True)
    ninios = models.IntegerField(default=0, null=True, blank=True)
    monto =  models.FloatField(null=True, blank=True)
    telefono = models.IntegerField(null=True, blank=True)
    comentario = models.CharField(max_length=150, blank=True, null=True)
    reserva_cod = models.CharField(max_length=100, default="null")
    estado = models.IntegerField(default=2, help_text= 'Anulada 0, Confirmada 1, Pendiente 2')


    def __str__(self):
        return f'El usuario:  {self.user.username} reserva habitacion: {self.room}'



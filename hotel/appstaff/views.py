from django.shortcuts import render,redirect, get_object_or_404, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required # para proteger las rutas
from django.contrib import messages
from django.db import IntegrityError
from .models import CategoriaHabitacion, Habitacion, Reserva
#importo el formulario
from .forms import CatHabitacionForm, HabitacionForm, ReservaForm
from django.contrib.auth.decorators import login_required # para proteger las rutas
from datetime import datetime,date
from django.template import loader
from django.template.response import TemplateResponse
#from payments import get_payment_model, RedirectNeeded
'''
def payment_details(request, payment_id):
    payment = get_object_or_404(get_payment_model(), id=payment_id)

    try:
        form = payment.get_form(data=request.POST or None)
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))

    return TemplateResponse(
        request,
        'payment.html',
        {'form': form, 'payment': payment}
    )'''

# Create your views here.
## templates de Python Hotel
def index(request):
    return render(request, 'index.html', {})
def habitaciones(request):
    return render(request, 'habitaciones.html', {} )

def reservas(request):
    return render(request, 'reservas.html', {} )

def servicios(request):
    return render(request, 'servicios.html', {} )

def contacto(request):
    return render(request, 'contacto.html', {} )
def doble(request):
    return render(request, 'doble.html', {} )
def galeria_entretenimientos(request):
    return render(request, 'galeria_entretenimientos.html', {} )
def galeria_espacios(request):
    return render(request, 'galeria_espacios.html', {} )
def galeria_habitaciones(request):
    return render(request, 'galeria_habitaciones.html', {} )
def galeria_instalaciones(request):
    return render(request, 'galeria_instalaciones.html', {} )
def galeria(request):
    return render(request, 'galeria.html', {} )
def peliculas_a_la_carta(request):
    return render(request, 'peliculas_a_la_carta.html', {} )
def suite(request):
    return render(request, 'suite.html', {} )
def superior(request):
    return render(request, 'superior.html', {} )
## end funciones python hotel ##


#### Esta es la fcion de buscar habitaciones ###
def reservar_1(request):
    #rooms = Habitacion.objects.all()
    categorias = CategoriaHabitacion.objects.all()
    if request.method == 'POST':
        try:
            #print(request.POST)
            rr = []
            for each_book in Reserva.objects.all():
                if str(each_book.check_in) < str(request.POST['check_in']) and str(each_book.check_out) < str(request.POST['check_out']): 
                    pass
                elif str(each_book.check_in) > str(request.POST['check_in']) and str(each_book.check_out) > str(request.POST['check_out']): 
                    pass
                else:
                    rr.append(each_book.room.id)
            personas = int(request.POST['adultos']) + int(request.POST['ninios'])
            #print(personas)
            rooms = Habitacion.objects.all().filter(capacidad__gte = int(personas)).exclude(id__in=rr)
            #print(rr)
            print(rooms)
            if len(rooms) == 0:
                messages.warning(request,'Perdón no hay habitaciones disponibles en esas fechas')
            checkin = request.POST['check_in']
            checkout = request.POST['check_out']
            adultos = request.POST['adultos']
            ninios = request.POST['ninios']
            print(checkin)
            ctx = {'rooms': rooms,
            'categorias': categorias,
            'checkin':checkin,
            }
            #print(data)
            #template = 'reservar.html'
            #loader.get_template('reservar.html')
            #return HttpResponse(template.render(ctx,request))
            return render(request,'reservar_1.html', {'checkin': checkin, 'checkout': checkout, 'adultos': adultos, 'ninios': ninios,'rooms': rooms, 'categorias': categorias})

        except Exception as e:
            messages.error(request,e)
            response = render(request, 'reservar_1.html', {})

    else:
        #data = {'rooms': rooms}
        response = render(request, 'reservar_1.html', {'categorias': categorias
        })

    return HttpResponse(response)

#### reserva y graba la reserva ###

def booking_room(request, roomid, checkin, checkout, adultos, ninios):
    room = Habitacion.objects.all().get(id=roomid)
    categoria = CategoriaHabitacion.objects.all().get(nombre=room.categoria)
    #print(categoria)
    if request.method == "POST":
        #room_id = request.POST['room_id']
        room = Habitacion.objects.all().get(id=roomid)
        #checkin = request.POST['check_in']
        
        date_checkin = datetime.strptime(checkin, '%Y-%m-%d')
       # checkout = request.POST['check_out']
        date_checkout = datetime.strptime(checkout, '%Y-%m-%d')
        #print((checkin))
       # days = (date_checkout-date_checkin).days
        days = (date_checkout-date_checkin).days
        print(days)
        price = days * room.precio
        #para encontar las habitaciones reservadas en el mismo periodo de tiempo para excluirlas
        '''for each_book in Reserva.objects.all().filter(room = room):
            if str(each_book.check_in) < str(request.POST['check_in']) and str(each_book.check_out) < str(request.POST['check_out']):
                pass
            elif str(each_book.check_in) > str(request.POST['check_in']) and str(each_book.check_out) > str(request.POST['check_out']):
                pass
            else:
                messages.warning(request,"Sorry This Room is unavailable for Booking")
                return redirect("reservar_1")'''
        current_user = request.user
        #total_person = int(request.POST['person'])
        reserva_cod = str(roomid) + str(date.today())
        print(reserva_cod)
        reserva = Reserva()
        room_object = Habitacion.objects.all().get(id=roomid)
        room_object.estado = 0
        room_object.save()
        user_object = User.objects.all().get(username=current_user)
        reserva.user = user_object
        reserva.check_in = checkin
        reserva.check_out = checkout
        reserva.monto = price
        reserva.room = room
        reserva.adultos = int(adultos)
        reserva.ninios = int(ninios)
        reserva.reserva_cod = reserva_cod
        reserva.telefono = int(request.POST['telefono'])
        reserva.comentario =request.POST['comentario']


        reserva.save()
        print(reserva)
        messages.success(request,'Felicitaciones! Reserva exitosa')
        return render(request, 'confirm.html', {
            'room': room,
            'booking': reserva,
            'days': days,
            'price': price,
        })
    else:
         return render(request, 'book_room.html', {
        'room':room,
        'categoria': categoria,
        'checkin':checkin,
        'checkout': checkout,
        'adultos': adultos,
        'ninios': ninios
    })

### Busca y muestra reservas del user ####
def books_user(request):
    context = {}
    
    usuario = request.user
    #print(usuario)
    books = Reserva.objects.filter(user=usuario)
    #print(books)
    categorias = CategoriaHabitacion.objects.all()
    rooms = Habitacion.objects.all()
    now = datetime.now().date()
    
    #print(type(now))
    book_list = []
    for book in books:
        fecha_check_in = book.check_in
        #print((fecha_check_in))
        if fecha_check_in:

            if fecha_check_in >= now:
                book_list.append(book)

            else:
                pass
        else:
            pass
    #print(book_list)
    context = {
            'books': books,
            'reservas': book_list,
            'rooms': rooms,
            'categorias' : categorias,
            'now': now,
    }

    return render(request, 'books_user.html', {
        'books': books,
        'reservas': book_list,
        'rooms': rooms,
        'categorias': categorias,
        'now': now,
    })   
### Cancela la reserva la pone en estado 0 ####    
def cancel_book(request, id):
    reserva = Reserva.objects.get(id=id)

    reserva.estado = 0
    reserva.save()
    return redirect('index')

#### esta ya no la uso ####
'''
def reservar(request):
    #rooms = Habitacion.objects.all()
    categorias = CategoriaHabitacion.objects.all()
    if request.method == 'POST':
        try:
            #print(request.POST)
            rr = []
            for each_book in Reserva.objects.all():
                if str(each_book.check_in) < str(request.POST['check_in']) and str(each_book.check_out) < str(request.POST['check_out']): 
                    pass
                elif str(each_book.check_in) > str(request.POST['check_in']) and str(each_book.check_out) > str(request.POST['check_out']): 
                    pass
                else:
                    rr.append(each_book.room.id)
            personas = int(request.POST['adultos']) + int(request.POST['ninios'])
            #print(personas)
            rooms = Habitacion.objects.all().filter(capacidad__gte = int(personas)).exclude(id__in=rr)
            #print(rr)
            print(rooms)
            if len(rooms) == 0:
                messages.warning(request,'Perdón no hay habitaciones disponibles en esas fechas')
            checkin = request.POST['check_in']
            checkout = request.POST['check_out']
            adultos = request.POST['adultos']
            ninios = request.POST['ninios']
            print(checkin)
            ctx = {'rooms': rooms,
            'categorias': categorias,
            'checkin':checkin,
            }
            #print(data)
            #template = 'reservar.html'
            #loader.get_template('reservar.html')
            #return HttpResponse(template.render(ctx,request))
            return render(request,'reservar.html', {'checkin': checkin, 'rooms': rooms, 'categorias': categorias})

        except Exception as e:
            messages.error(request,e)
            response = render(request, 'reservar.html', {})

    else:
        #data = {'rooms': rooms}
        response = render(request, 'reservar.html', {'categorias': categorias
        })

    return HttpResponse(response)
'''
'''
def book_room_page(request):
    room = Habitacion.objects.all().get(id=int(request.GET['roomid']))
    checkin = request.GET['checkin']
    categoria = CategoriaHabitacion.objects.all().get(nombre=room.categoria)
    #print(categoria)
    
    return render(request, 'book_room.html', {
        'room':room,
        'categoria': categoria,
        'checkin':checkin
    })

def book_room(request):
    if request.method == "POST":
        room_id = request.POST['room_id']
        room = Habitacion.objects.all().get(id=room_id)
        checkin = request.POST['check_in']
        
        date_checkin = datetime.strptime(checkin, '%Y-%m-%d')
        checkout = request.POST['check_out']
        date_checkout = datetime.strptime(checkout, '%Y-%m-%d')
        #print((checkin))
        days = (date_checkout-date_checkin).days
        print(days)
        price = days * room.precio
        #para encontar las habitaciones reservadas en el mismo periodo de tiempo para excluirlas
        for each_book in Reserva.objects.all().filter(room = room):
            if str(each_book.check_in) < str(request.POST['check_in']) and str(each_book.check_out) < str(request.POST['check_out']):
                pass
            elif str(each_book.check_in) > str(request.POST['check_in']) and str(each_book.check_out) > str(request.POST['check_out']):
                pass
            else:
                messages.warning(request,"Sorry This Room is unavailable for Booking")
                return redirect("reservar")
        current_user = request.user
        total_person = int(request.POST['person'])
        reserva_id = str(room_id) + str(date.today())
        print(reserva_id)
        reserva = Reserva()
        room_object = Habitacion.objects.all().get(id=room_id)
        room_object.estado = 0
        room_object.save()
        user_object = User.objects.all().get(username=current_user)
        reserva.user = user_object
        reserva.check_in = request.POST['check_in']
        reserva.check_out = request.POST['check_out']
        reserva.monto = price
        reserva.room = room
        reserva.adultos = int(request.POST['adultos'])
        reserva.ninios = int(request.POST['ninios'])
        reserva.reserva_id = reserva_id
        reserva.telefono = int(request.POST['telefono'])
        reserva.comentario =request.POST['comentario']


        reserva.save()
        print(reserva)
        messages.success(request,'Felicitaciones! Reserva exitosa')
        return render(request, 'confirm.html', {
            'room': room,
            'booking': reserva,
            'days': days,
            'price': price,
        })
    else:
        return HttpResponse('no se pudo hacer')
'''
### muestra los datos de la reserva en confirm.html ###
def confirmar(request, pk):
    try:
        booking = Reserva.objects.latest()
        print(booking)
        room = Habitacion.objects.get(pk=pk)
        
        days = (booking.check_out-booking.check_in).days
        
        price = days * room.precio
        print(price)
        print(room.pk)
       
        context = {
            'room': room,
            'booking': booking,
            'days': days,
            'price': price,
        }
    except:
        pass
    return render(request, 'confirm.html', {
        'room': room,
        'booking': booking,
        'days': days,
        'precio': price
    })

### muestra reserva exitosa ###
def success(request, id):
    book = Reserva.objects.all().get(id=id)
    print(book)
    return render(request,'success.html',{
        'book': book
    })


### funciones de signin User ###
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm,
        })
        # print("enviando el formulario")
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # intento guardar user
                user = User.objects.create_user(
                    username=request.POST['username'], 
                    password=request.POST['password1'],
                    first_name=request.POST['first_name'],
                    last_name = request.POST['last_name'],
                    email = request.POST['email']
                    )
                user.save()
                login(request, user)  # abro sesion de user
                return redirect('index')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exists'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Password do not match'
        })  # print(request.POST)
    # print("obteniendo datos")

@login_required
def signout(request):
    logout(request)
    return redirect('index')


def signin(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': AuthenticationForm
        })
    else:
        # autentica usario y password
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        # print(request.POST)
        if user is None:  # usuario no valido
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:  # ususario y password correctos
            login(request, user)  # guardo sesion user
            return redirect('index')


''' modulo staff '''
#### Staff ####
def categoria_habitacion(request):
    total_categorias = CategoriaHabitacion.objects.count()
    categorias = CategoriaHabitacion.objects.all()
    return render(request, 'categoria_habitacion_list.html', {
        'categorias' : categorias,
        'cantidad': total_categorias
    })
def habitacion_list(request):
    habitaciones = Habitacion.objects.all()
    categorias = CategoriaHabitacion.objects.all()
    total_habitaciones = Habitacion.objects.count()
    return render(request, 'habitacion_list.html', {
        'habitaciones' : habitaciones,
        'categorias' : categorias,
        'cantidad': total_habitaciones,
    })
def usuarios_list(request):
    usuarios = User.objects.all()
   
    total_usuarios = User.objects.count()
    return render(request, 'usuarios_list.html', {
        'usuarios' : usuarios,
        'cantidad': total_usuarios,
    })
def reservas_list(request):
    reservas = Reserva.objects.all()
    habitaciones = Habitacion.objects.all()

    categorias = CategoriaHabitacion.objects.all()
    total_reservas = Reserva.objects.count()
    return render(request, 'reservas_list.html', {
        'reservas' : reservas,
        'habitaciones': habitaciones,
        'categorias' : categorias,
        'cantidad': total_reservas,
    })
def book(request):
    reservas = Reserva.objects.all()
    habitaciones = Habitacion.objects.all()
    categorias = CategoriaHabitacion.objects.all()
    total_reservas = Reserva.objects.count()
    return render(request, 'book.html', {
        'reservas': reservas,
        'categorias': categorias,
        'cantidad': total_reservas,
        'habitaciones': habitaciones
    })

## crear editar borrar reservas STAFF ##
def create_book(request):
    form = ReservaForm()

    if request.method == "POST":
        form = ReservaForm(request.POST)
        #if form.check_in >= form.check_out:

        #    return redirect('/create_book')
        #else:
        if form.is_valid():
            new_book = form.save(commit=False)
            new_book.user = request.user
           
            new_book.save()
            #form.save()
            return redirect('/room')
        
    ctx = {
        'form': form,
        'value': 'RESERVAR'
    }
    return render(request, 'create_book.html', ctx )




def edit_book(request, id):
    reserva = Reserva.objects.get(id=id)
    form = ReservaForm(instance= reserva)

    if request.method == 'POST':
        form = ReservaForm(request.POST, instance =reserva)
        if form.is_valid():
            form.save()
            return redirect('confirm', pk = reserva.id)


    return render(request, 'create_book.html', {
        'form': form,
        'value': 'EDITAR'
    })   
    
def delete_book(request, id):
    reserva = Reserva.objects.get(id=id)

    reserva.delete()
    return redirect('books_user')



   


@login_required
def book_detail(request, id):
    if request.method == 'GET':
        # print(task_id)
        # por si preguntan x una tarea q no existe
        reserva = get_object_or_404(Reserva, pk=id, user = request.user)
        form = ReservaForm(instance=reserva)
        return render(request, 'book_detail.html', {
            'reserva': reserva,
            'form': form
        })
    else:
        try:
            reserva = get_object_or_404(Reserva, pk=id, user = request.user)
            form = ReservaForm(request.POST, instance=reserva)
            form.save() #graba modificado
            return redirect('/index')
        except ValueError:
            return render(request, 'book_detail.html', {
            'reserva': reserva,
            'form': form,
            'error': 'Error updtaing Rserva'
        })
## crear editar borrar resrvas Staff App ##
def create_reserva(request):
    form = ReservaForm()

    if request.method == "POST":
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/reservas_list')

    ctx = {
        'form': form,
        'value': 'CREAR'
    }
    return render(request, 'create_reserva.html', ctx )

def edit_reserva(request, id):
    reserva = Reserva.objects.get(id=id)
    form = ReservaForm(instance=reserva)

    if request.method == 'POST':
        form = ReservaForm(request.POST, instance = reserva)
        if form.is_valid():
            form.save()
            return redirect('/reservas_list')

    return render(request, 'create_reserva.html', {
        'form': form,
        'value': 'EDITAR'
    })   

def delete_reserva(request, id):
    reserva = Reserva.objects.get(id=id)

    if request.method == 'POST':
        reserva.delete()
        return redirect('/reservas_list')
    ctx = {
        'reserva' : reserva
        } 

    return render(request, 'delete_reserva.html', ctx)


## crear editar borrar usuarios Staff App ##
def create_usuario(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/usuarios_list')

    ctx = {
        'form': form,
        'value': 'CREAR'
    }
    return render(request, 'create_usuario.html', ctx )

def edit_usuario(request, id):
    usuario = Habitacion.objects.get(id=id)
    form = UserCreationForm(instance=usuario)

    if request.method == 'POST':
        form = UserCreationForm(request.POST, instance = usuario)
        if form.is_valid():
            form.save()
            return redirect('/usuarios_list')

    return render(request, 'create_usuario.html', {
        'form': form,
        'value': 'EDITAR'
    })   

def delete_usuario(request, id):
    usuario = User.objects.get(id=id)

    if request.method == 'POST':
        usuario.delete()
        return redirect('/usuarios_list')
    ctx = {
        'usuario' : usuario
        } 

    return render(request, 'delete_usuario.html', ctx)



## crear editar borrar habitaciones Staff App ##
def create_habitacion(request):
    form = HabitacionForm()

    if request.method == "POST":
        form = HabitacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/habitacion_list')

    ctx = {
        'form': form,
        'value': 'CREAR'
    }
    return render(request, 'create_habitacion.html', ctx )

def edit_habitacion(request, id):
    habitacion = Habitacion.objects.get(id=id)
    form = HabitacionForm(instance=habitacion)

    if request.method == 'POST':
        form = HabitacionForm(request.POST, instance = habitacion)
        if form.is_valid():
            form.save()
            return redirect('/habitacion_list')

    return render(request, 'create_habitacion.html', {
        'form': form,
        'value': 'EDITAR'
    })   

def delete_habitacion(request, id):
    habitacion = Habitacion.objects.get(id=id)

    if request.method == 'POST':
        habitacion.delete()
        return redirect('/habitacion_list')
    ctx = {
        'habitacion' : habitacion
        } 

    return render(request, 'delete_habitacion.html', ctx)




## crear editar borrar categorias Staff App ##
def create_cat_habitacion(request):
    form = CatHabitacionForm()

    if request.method == "POST":
        form = CatHabitacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/categoria_habitacion')

    ctx = {
        'form': form,
        'value': 'CREAR'
    }
    return render(request, 'create_categoria.html', ctx )

def edit_cat_habitacion(request, id):
    categoria = CategoriaHabitacion.objects.get(id=id)
    form = CatHabitacionForm(instance=categoria)

    if request.method == 'POST':
        form = CatHabitacionForm(request.POST, instance = categoria)
        if form.is_valid():
            form.save()
            return redirect('/categoria_habitacion')

    return render(request, 'create_categoria.html', {
        'form': form,
        'value': 'EDITAR'
    })   

def delete_cat_habitacion(request, id):
    categoria = CategoriaHabitacion.objects.get(id=id)

    if request.method == 'POST':
        categoria.delete()
        return redirect('/categoria_habitacion')
    ctx = {
        'categoria' : categoria
        } 

    return render(request, 'delete_categoria.html', ctx)


#### no uso ####
'''
def reservas(request):
    if request.method == 'POST':
        check_in = request.POST['check_in']
        check_out = request.POST['check_out']
        adultos = request.POST['adultos']
        user = request.user
        ninios = request.POST['ninios']
        telefono = request.POST['telefono']
        comentario = request.POST['comentario']
        book = Reserva.objects.create( check_in = check_in, check_out =     check_out, adultos = adultos, ninios = ninios, telefono = telefono,     comentario = comentario, user = user)
        print(book)
        return redirect('room')
    else:
        return render(request, 'reservas.html', {} )
'''
'''
def editar_book(request, id):
    
    reserva = Reserva.objects.all().get(id=id)
    room = Habitacion.objects.all().get(id=reserva.room_id)
    categorias = CategoriaHabitacion.objects.all()

    #print(reserva.check_in)
    if request.method == "POST":
        room_id = request.POST['room_id']
        room = Habitacion.objects.all().get(id=room_id)
        checkin = request.POST['check_in']
        
        date_checkin = datetime.strptime(checkin, '%Y-%m-%d')
        checkout = request.POST['check_out']
        date_checkout = datetime.strptime(checkout, '%Y-%m-%d')
        #print((checkin))
        days = (date_checkout-date_checkin).days
        print(days)
        price = days * room.precio
        
        for each_book in Reserva.objects.all().filter(room = room):
            if str(each_book.check_in) < str(request.POST['check_in']) and str(each_book.check_out) < str(request.POST['check_out']):
                pass
            elif str(each_book.check_in) > str(request.POST['check_in']) and str(each_book.check_out) > str(request.POST['check_out']):
                pass
            else:
                messages.warning(request,"Sorry This Room is unavailable for Booking")
                return redirect("modificar")
        current_user = request.user
        total_person = int(request.POST['person'])
        #reserva = Reserva()
      
        user_object = User.objects.all().get(username=current_user)
        reserva.user = user_object
        reserva.check_in = request.POST['check_in']
        reserva.check_out = request.POST['check_out']
        reserva.monto = price
        reserva.room = room
        reserva.adultos = int(request.POST['adultos'])
        reserva.ninios = int(request.POST['ninios'])
        reserva.reserva_id = reserva.reserva_id
        reserva.telefono = int(request.POST['telefono'])
        reserva.comentario =request.POST['comentario']


        reserva.save()
        print(reserva)
        messages.success(request,'Felicitaciones! Reserva modificada')
        return render(request, 'confirm.html', {
            'room': room,
            'booking': reserva,
            'days': days,
            'price': price,
            
        })
    else:
       return render(request, 'modificar.html', {
        'reserva': reserva,
        'room': room,
        'categorias': categorias,
        
    })

 

def editar_room(request, id):
    categorias = CategoriaHabitacion.objects.all()
    reserva = Reserva.objects.all().get(id=id)
    if reserva:

        rr = []
        for each_book in Reserva.objects.all():
            if str(each_book.check_in) < str(reserva.check_in) and str(each_book.check_out) < str(reserva.check_out): 
                pass
            elif str(each_book.check_in) > str(reserva.check_in) and str(each_book.check_out) > str(reserva.check_out): 
                pass
            else:
                rr.append(each_book.room.id)
        personas = int(reserva.adultos) + int(reserva.ninios)
            #print(personas)
        room = Habitacion.objects.all().filter(capacidad__gte = int(personas)).exclude(id__in=rr)
            #print(rr)
        print(room)
        if len(room) == 0:
         messages.warning(request,'Perdón no hay habitaciones disponibles en esas fechas')
        checkin = reserva.check_in
        checkout = reserva.check_out
        print(checkin)
        data = {'rooms': room,
            'categorias': categorias,
            'checkin' : checkin,
            'checkout' : checkout}
        print(data)
        return render(request,'modificar_room.html',{
            'rooms': room,
            'categorias': categorias,
            })
    else:
        return render(request, 'modificar.html', {})

       

   

   
    
    form = ReservaForm(request.POST, instance = reserva)
    #print(form)
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance =  reserva)
       
        if form.is_valid():
            form.save()
            return redirect('/fare')
    return render(request, 'modificar.html' , {
        'reserva': reserva,
        'categorias': categorias, 'room': room
        
    })'''
 



'''
def room(request):
    context = {}
    try:
        booking = Reserva.objects.latest()
        categorias = CategoriaHabitacion.objects.all()
        #print(categorias)
        rooms = Habitacion.objects.all()
        
        days = booking.check_out-booking.check_in
        avail_list = []
        for room in rooms:
            if room.estado == 1:
                avail_list.append(room)
            else:
                pass
        
        context = {
            'room': avail_list,
            'booking': booking,
            'days': days,
            'categorias' : categorias
        }
    except:
        pass
    return render(request, 'room.html', context)

def room(request):
    context = {}
    try:
        booking = Reserva.objects.latest()
        categorias = CategoriaHabitacion.objects.all()
        #print(categorias)
        rooms = Habitacion.objects.all()
        
        days = booking.check_out-booking.check_in
        avail_list = []
        for room in rooms:
            if room.estado == 1:
                avail_list.append(room)
            else:
                pass
        
        context = {
            'room': avail_list,
            'booking': booking,
            'days': days,
            'categorias' : categorias
        }
    except:
        pass
    return render(request, 'room.html', context)
def fare(request, pk):
    try:
        booking = Reserva.objects.latest()
        print(booking)
        room = Habitacion.objects.get(pk=pk)
        print(room)
        days = (booking.check_out-booking.check_in).days
        
        price = days * room.precio
        print(price)
        print(room.pk)
        room.estado = 0
        booking.room = room.pk
        print(room.numero)
        booking.monto = price
        booking.user = request.user
        print(booking)
        booking.save()
        room.save()
        context = {
            'room': room,
            'booking': booking,
            'days': days,
            'price': price,
        }
    except:
        pass
    return render(request, 'fare.html', {
        'room': room,
        'booking': booking,
        'days': days,
        'precio': price
    })
'''
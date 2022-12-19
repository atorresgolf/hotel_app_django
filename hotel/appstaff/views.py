from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required # para proteger las rutas
from django.db import IntegrityError
from .models import CategoriaHabitacion, Habitacion, Reserva
#importo el formulario
from .forms import CatHabitacionForm, HabitacionForm, ReservaForm
from django.contrib.auth.decorators import login_required # para proteger las rutas
from datetime import datetime,date


# Create your views here.
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

## crear editar borrar reservas ##
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
def fare(request, pk):
    try:
        booking = Reserva.objects.latest()
        print(booking)
        room = Habitacion.objects.get(pk=pk)
        
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
def success(request):
    
    return render(request,'success.html',{})

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
def editar_book(request):
    usuario = request.user
    reserva = Reserva.objects.filter(user = usuario).latest()
    
   
    form = ReservaForm(request.POST, instance = reserva)
    #print(form)
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance =  reserva)
       
        if form.is_valid():
            form.save()
            return redirect('/fare')
    return render(request, 'create_book.html', {
        'form': form,
        'value': 'EDITAR'
    })
    
def delete_book(request, id):
    reserva = Reserva.objects.get(id=id)

    if request.method == 'POST':
        reserva.delete()
        return redirect('/habitacion_list')
    ctx = {
        'reserva' : reserva
        } 

    return render(request, 'delete_book.html', ctx)

''' modulo staff '''
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
## crear editar borrar resrvas ##
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


## crear editar borrar usuarios ##
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



## crear editar borrar habitaciones ##
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




## crear editar borrar categorias ##
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
# funciones de signin
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



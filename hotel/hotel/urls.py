"""hotel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from appstaff import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('categoria_habitacion/', views.categoria_habitacion, name= 'categoria_habitacion'),
    path('create_cat_habitacion/', views.create_cat_habitacion, name='create_cat_habitacion'),
    path('edit_cat_habitacion/<int:id>', views.edit_cat_habitacion, name = 'edit_cat_habitacion'),
    path('delete_cat_habitacion/<int:id>', views.delete_cat_habitacion, name = 'delete_cat_habitacion'),    
    path('habitacion_list/', views.habitacion_list, name= 'habitacion_list'),
    path('create_habitacion/', views.create_habitacion, name='create_habitacion'),
    path('edit_habitacion/<int:id>', views.edit_habitacion, name = 'edit_habitacion'),
    path('delete_habitacion/<int:id>', views.delete_habitacion, name = 'delete_habitacion'), 
    path('usuarios_list/', views.usuarios_list, name= 'usuarios_list'),
    path('create_usuario/', views.create_usuario, name='create_usuario'),
    path('edit_usuario/<int:id>', views.edit_usuario, name = 'edit_usuario'),
    path('delete_usuario/<int:id>', views.delete_usuario, name = 'delete_usuario'), 
    path('book/', views.book, name= 'book'),
    path('create_book/', views.create_book, name='create_book'),
    path('reservar_1/', views.reservar_1, name='reservar_1'),

 
    path('booking_room/<int:roomid>/<str:checkin>/<str:checkout>/<int:adultos>/<int:ninios>', views.booking_room, name='booking_room'),
    path('cancel_book/<int:id>/', views.cancel_book, name = 'cancel_book'),

    path('edit_book/<int:id>/', views.edit_book, name = 'edit_book'),
    path('delete_book/<int:id>/', views.delete_book, name = 'delete_book'),
    path('book_detail/<int:id>/', views.book_detail, name='book_detail'),
    path('books_user/',views.books_user , name="books_user"),
    path('confirm/<int:pk>', views.confirmar, name ='confirmar'),
    path('<int:pk>/', views.confirmar, name='confirmar'),
    path('success/<int:id>', views.success, name="success"),
    path('habitaciones/', views.habitaciones, name='habitaciones'),
    path('reservas/', views.reservas, name='reservas'),
    path('reservas_list/', views.reservas_list, name='reservas_list'),
    path('create_reserva/', views.create_reserva, name='create_reserva'),
    path('edit_reserva/<int:id>', views.edit_reserva, name = 'edit_reserva'),
    path('delete_reserva/<int:id>', views.delete_reserva, name = 'delete_reserva'), 
    path('servicios/', views.servicios, name='servicios'),
    path('contacto/', views.contacto, name='contacto'),
    path('doble/', views.doble , name='doble'),
    path('galeria_entretenimientos/', views.galeria_entretenimientos , name='galeria_entretenimientos'),
    path('galeria_espacios/', views.galeria_espacios , name='galeria_espacios'),
    path('galeria_habitaciones/', views.galeria_habitaciones , name='galeria_habitaciones'),
    path('galeria_instalaciones/', views.galeria_instalaciones , name='galeria_instalaciones'),
    path('galeria/', views.galeria , name='galeria'),
    path('peliculas_a_la_carta', views.peliculas_a_la_carta, name='peliculas_a_la_carta'),
    path('suite/', views.suite , name='suite'),
    path('superior/', views.superior , name='superior'),
    path('signup/', views.signup, name='signup' ),
    path('logout/', views.signout, name='logout' ),
    path('login/', views.signin, name='login' ),
    #path('reservar/', views.reservar, name='reservar'),
   # path('payments/', include('payments.urls')),
    #path('__debug__/', include('debug_toolbar.urls')),
  # path('book_room/', views.book_room_page, name='book_room_page'),
   # path('book_room/book', views.book_room, name='book_room'),
  # path('editar_book/<int:id>/', views.editar_book, name='editar_book'),
  #  path('editar_room/<int:id>/', views.editar_room, name='editar_room'),

    #path('room/',views.room , name="room"),
   # path('confirm/<int:pk>', views.fare, name ='confirm'),
   # path('<int:pk>/', views.fare, name='fare'),
 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
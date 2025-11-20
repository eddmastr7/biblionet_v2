from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    # 1. Ruta principal del catálogo con búsqueda y filtro
    path('catalogo/', views.catalogo_view, name='catalogo_url'), 
    
    # 2. Ruta para ver los detalles del libro ('Ver Ficha')
    path('libro/<int:pk>/', views.ficha_libro, name='ficha_libro'),
    
    # 3. Ruta para procesar la reserva (POST)
    path('reservar/<int:libro_pk>/', views.solicitar_reserva, name='solicitar_reserva'), 
    
    # ¡NUEVA RUTA! 4. Listado de Reservas del Cliente
    path('mis-reservas/', views.listado_reservas_view, name='listado_reservas'), 
]
=======
    path("inicio_sesion/empleado/", views.iniciar_sesion_empleado, name="inicio_sesion"),
    path("salir/", views.cerrar_sesion_empleado, name="cerrar_sesion"),
    path("pantalla_inicio/administrador/", views.panel_administrador, name="panel_administrador"),
    path("pantalla_inicio/bibliotecario/", views.panel_bibliotecario, name="panel_bibliotecario"),
    path("empleados/registrar/", views.registrar_empleado, name="registrar_empleado"),
    path("empleados/inventario/",views.inventario, name="inventario"),

    path("clientes/historial/", views.historial_cliente, name="historial_cliente"),
    path("registro/prestamo/", views.registrar_prestamo, name= "registrar_prestamo")

    
]
>>>>>>> feat-inventario

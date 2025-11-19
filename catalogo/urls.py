# catalogo/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # 1. Ruta principal del catálogo con búsqueda y filtro
    path('catalogo/', views.catalogo_view, name='catalogo_url'), 
    
    # 2. Ruta para ver los detalles del libro ('Ver Ficha')
    path('libro/<int:pk>/', views.ficha_libro, name='ficha_libro'),
    
    # ¡NUEVO! 3. Ruta para procesar la reserva
    path('reservar/<int:libro_pk>/', views.solicitar_reserva, name='solicitar_reserva'), 
]
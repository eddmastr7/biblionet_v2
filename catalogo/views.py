# catalogo/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q 
from django.contrib.auth.decorators import login_required
from django.contrib import messages # Necesario para notificaciones al usuario
from django.utils import timezone
from datetime import timedelta
from .models import Libro, Reserva # Asegúrate de que Reserva esté importado

# VISTA DE RESERVA (IMPLEMENTACIÓN COMPLETA)
@login_required 
def solicitar_reserva(request, libro_pk):
    if request.method == 'POST':
        libro = get_object_or_404(Libro, pk=libro_pk)
        cliente = request.user
        
        # Validación de que el libro realmente esté prestado antes de reservar
        if libro.disponible:
            messages.warning(request, f'El libro "{libro.titulo}" está disponible y no requiere reserva.')
            return redirect('ficha_libro', pk=libro_pk)
        
        # 1. CRITERIO: Máximo 2 reservas activas por cliente
        # 'activo=True' es un campo que DEBES añadir al modelo Reserva para esta lógica
        reservas_activas_cliente = Reserva.objects.filter(cliente=cliente, activa=True, retirado=False).count()
        if reservas_activas_cliente >= 2:
            messages.error(request, 'No puedes tener más de 2 reservas activas al mismo tiempo.')
            return redirect('ficha_libro', pk=libro_pk)

        # 2. Prevenir reservas duplicadas del mismo libro
        if Reserva.objects.filter(cliente=cliente, libro=libro, activa=True, retirado=False).exists():
            messages.info(request, f'Ya tienes una reserva activa para el libro "{libro.titulo}".')
            return redirect('ficha_libro', pk=libro_pk)

        # 3. Crear la Reserva (Cola FIFO)
        # La 'fecha_reserva' (auto_now_add=True) se usa para el orden FIFO
        Reserva.objects.create(
            cliente=cliente, 
            libro=libro,
        )
        
        messages.success(request, f'¡Reserva del libro "{libro.titulo}" creada con éxito! Estás en la lista de espera.')
        
    return redirect('ficha_libro', pk=libro_pk) # Redirige a la ficha del libro


# VISTA DE CATÁLOGO (sin cambios)
def catalogo_view(request):
    # ... (Tu código actual de catalogo_view)
    libros = Libro.objects.all()
    query = request.GET.get('q')
    disponible_filter = request.GET.get('disponible')
    
    if query:
        libros = libros.filter(Q(titulo__icontains=query) | Q(autor__icontains=query))
    if disponible_filter == 'si':
        libros = libros.filter(disponible=True)
    elif disponible_filter == 'no':
        libros = libros.filter(disponible=False)
        
    context = {'libros': libros, 'query': query}
    return render(request, 'catalogo/catalogo.html', context)


# VISTA DE FICHA (sin cambios)
def ficha_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    context = {'libro': libro}
    return render(request, 'catalogo/ficha_libro.html', context)
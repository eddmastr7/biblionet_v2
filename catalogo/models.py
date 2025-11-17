# catalogo/models.py
from django.db import models

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    # Este campo es clave para el filtrado de disponibilidad.
    disponible = models.BooleanField(default=True) 
    
    # Otros campos no sensibles como:
    # editorial = models.CharField(max_length=100)
    # fecha_publicacion = models.DateField()
    
    def __str__(self):
        return self.titulo

# Nota: Si modificaste models.py, debes ejecutar: 
# python manage.py makemigrations catalogo
# python manage.py migrate
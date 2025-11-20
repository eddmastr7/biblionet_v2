from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
<<<<<<< HEAD
=======

from biblio import views
>>>>>>> feat-inventario

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("biblio.urls")),      # Inicio, catálogo, login cliente…
    path("", include("seguridad.urls")),   # Login empleados y panel 
    path("prestamos/registrar/", views.registrar_prestamo, name="registrar_prestamo"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
<<<<<<< HEAD


=======
>>>>>>> feat-inventario

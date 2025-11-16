from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("biblio.urls")),      # Inicio, catálogo, login cliente…
    path("seguridad/", include("seguridad.urls")),   # Login empleados y panel admin
    

]

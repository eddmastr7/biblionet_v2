from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("biblio.urls")),      # Inicio, catálogo, login cliente…
    path("", include("seguridad.urls")),   # Login empleados y panel admin
]

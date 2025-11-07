from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("catalogo/", views.catalogo, name="catalogo"),
    path("catalogo/fantasia/", views.catalogo_fantasia, name="fantasia"),
    path("acerca-de/", views.acerca_de, name="acerca_de"),

    path("login/cliente/", views.login_cliente, name="login_cliente"),
    path("registro/", views.registro_cliente, name="registro"),  # 👈 ESTA
]

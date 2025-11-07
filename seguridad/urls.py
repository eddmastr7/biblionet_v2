from django.urls import path
from . import views

urlpatterns = [
    path("login/empleado/", views.login_view, name="login"),
    path("salir/", views.logout_view, name="logout"),
    path("admin/", views.admin_home, name="admin_home"),
    path("empleado/", views.empleado_home, name="empleado_home"),
    path("empleados/registrar/", views.crear_empleado, name="registrar_empleado"),  # opcional, sólo admin
]

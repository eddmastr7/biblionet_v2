from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from biblio.models import Roles, Usuarios

class Command(BaseCommand):
    help = "Crea roles base y el administrador inicial"

    def handle(self, *args, **options):
        for nombre in ("administrador", "empleado"):
            obj, created = Roles.objects.get_or_create(nombre=nombre, defaults={"descripcion": nombre})
            self.stdout.write(self.style.SUCCESS(f"Rol {nombre}: {'creado' if created else 'ok'}"))

        rol_admin = Roles.objects.get(nombre="administrador")

        admin_email = "admin@biblionet.com"
        if not Usuarios.objects.filter(email=admin_email).exists():
            Usuarios.objects.create(
                rol=rol_admin,
                nombre="Admin",
                apellido="General",
                email=admin_email,
                clave=make_password("admin"),
                estado="activo",
            )
            self.stdout.write(self.style.SUCCESS(f"Admin creado: {admin_email} / admin"))
        else:
            self.stdout.write(self.style.WARNING("Admin ya existía"))

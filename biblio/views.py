from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.db import transaction
from biblio.models import Usuarios, Roles
from django.views.decorators.csrf import csrf_protect

def inicio(request):
    # Renderiza tu plantilla: biblio/templates/publico/pagina_inicio.html
    return render(request, "publico/pagina_inicio.html")

def catalogo(request):
    # Soporta búsqueda ?q=...
    q = (request.GET.get("q") or "").strip().lower()

    # Datos de ejemplo mientras conectas a la BD
    base = [
        {"titulo": "Harry Potter y la Piedra Filosofal", "autor": "J.K. Rowling", "descripcion": "Un niño descubre que es mago.", "disponible": True,  "imagen_url": ""},
        {"titulo": "El Señor de los Anillos", "autor": "J.R.R. Tolkien", "descripcion": "La épica del Anillo Único.",        "disponible": False, "imagen_url": ""},
        {"titulo": "Las Crónicas de Narnia", "autor": "C.S. Lewis",      "descripcion": "Aventuras en Narnia.",             "disponible": True,  "imagen_url": ""},
    ]

    if q:
        libros = [l for l in base if q in l["titulo"].lower() or q in l["autor"].lower() or q in (l["descripcion"] or "").lower()]
    else:
        libros = base

    ctx = {
        "libros": libros,
        "total_libros": len(libros),
    }
    # biblio/templates/publico/catalogo.html
    return render(request, "publico/catalogo.html", ctx)

def catalogo_fantasia(request):
    # Redirige a /catalogo/?q=fantasia para reutilizar la vista
    return redirect(f"{reverse('catalogo')}?q=fantasia")

def acerca_de(request):
    # Usa tu placeholder por ahora
    return render(request, "publico/placeholder.html")

def login_cliente(request):
    # biblio/templates/publico/login_cliente.html
    return render(request, "publico/login_cliente.html")

def registro(request):
    # Placeholder temporal para el botón "Registrarse"
    return render(request, "publico/placeholder.html")

def acerca_de(request):
    return render(request, "publico/acerca_de.html")

# Stub reutilizable para páginas aún no listas (si no lo tienes ya):
def placeholder(request):
    return render(request, "publico/placeholder.html")


def _password_ok(raw, stored):
    stored = stored or ""
    # Detecta hash común de Django
    if stored.startswith(("pbkdf2_", "argon2$", "bcrypt$")):
        return check_password(raw, stored)
    return raw == stored

def _usuarios_fieldnames():
    # Incluye sólo campos concretos (no M2M / reverse)
    return {
        f.name for f in Usuarios._meta.get_fields()
        if getattr(f, "concrete", False) and not getattr(f, "many_to_many", False) and not getattr(f, "one_to_many", False)
    }

# ---------- Registro de cliente ----------
def registro_cliente(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre","").strip()
        apellido = request.POST.get("apellido","").strip()
        dni = request.POST.get("dni","").strip()
        telefono = request.POST.get("telefono","").strip()
        email = request.POST.get("email","").strip().lower()
        password = request.POST.get("password","")
        confirm = request.POST.get("confirm_password","")

        ctx = {"form": request.POST.copy()}

        # Validaciones mínimas
        if not all([nombre, apellido, email, password, confirm]):
            ctx["error"] = "Completa todos los campos obligatorios."
            return render(request, "publico/registro_cliente.html", ctx)
        if len(password) < 8:
            ctx["error"] = "La contraseña debe tener al menos 8 caracteres."
            return render(request, "publico/registro_cliente.html", ctx)
        if password != confirm:
            ctx["error"] = "Las contraseñas no coinciden."
            return render(request, "publico/registro_cliente.html", ctx)
        if Usuarios.objects.filter(email=email).exists():
            ctx["error"] = "Ya existe una cuenta con ese correo."
            return render(request, "publico/registro_cliente.html", ctx)

        # Crear usuario cliente
        with transaction.atomic():
            rol, _ = Roles.objects.get_or_create(nombre="cliente")
            kwargs = dict(
                rol=rol,
                nombre=nombre,
                apellido=apellido,
                email=email,
                clave=make_password(password),
                estado="activo",
            )
            # Si tu modelo Usuarios tiene estos campos, se asignan; si no, omite estas líneas
            if hasattr(Usuarios, "dni"):
                kwargs["dni"] = dni
            if hasattr(Usuarios, "telefono"):
                kwargs["telefono"] = telefono

            usuario = Usuarios.objects.create(**kwargs)

        # Auto-login (sesión pública de cliente)
        request.session["cliente_id"] = usuario.id
        request.session["cliente_email"] = usuario.email
        messages.success(request, "¡Cuenta creada con éxito!")
        return redirect("catalogo")

    return render(request, "publico/registro_cliente.html")


@csrf_protect
def login_cliente(request):
    ctx = {}
    if request.method == "POST":
        email = request.POST.get("email","").strip().lower()
        password = request.POST.get("password","")

        try:
            user = Usuarios.objects.select_related("rol").get(
                email=email, rol__nombre="cliente", estado="activo"
            )
        except Usuarios.DoesNotExist:
            ctx["error"] = "Correo o contraseña incorrectos."
            return render(request, "publico/login_cliente.html", ctx)

        # Soporta hash y texto plano (por si tienes datos viejos)
        ok = False
        if user.clave:
            if user.clave.startswith(("pbkdf2_", "argon2$", "bcrypt$")):
                ok = check_password(password, user.clave)
            else:
                ok = (password == user.clave)

        if not ok:
            ctx["error"] = "Correo o contraseña incorrectos."
            return render(request, "publico/login_cliente.html", ctx)

        request.session["cliente_id"] = user.id
        request.session["cliente_email"] = user.email
        return redirect("catalogo")

    return render(request, "publico/login_cliente.html")
from functools import wraps

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import logout as auth_logout   # 👈 faltaba este import
from django.utils import timezone

from biblio.models import Usuarios, Roles, Libros, Prestamos


# ---------- Helpers de sesión / roles ----------
def _is_logged(request):
    return request.session.get("usuario_id") is not None

def _role(request):
    # "administrador" | "empleado" (según Roles.nombre)
    return request.session.get("rol")

def require_role(*allowed):
    """
    Redirige a 'login' si no hay sesión o si el rol no está permitido.
    """
    def deco(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if not _is_logged(request):
                return redirect("login")
            if _role(request) not in allowed:
                return redirect("login")
            return view(request, *args, **kwargs)
        return wrapper
    return deco

def _map_front_rol(rol_front: str) -> str:
    """
    Mapea el valor del <select> del form a Roles.nombre.
    Acepta: 'admin' -> 'administrador', 'empleado' -> 'empleado'.
    """
    if rol_front in ("admin", "administrador"):
        return "administrador"
    if rol_front == "empleado":
        return "empleado"
    return ""


# ---------- Login / Logout (empleados/admin) ----------
@csrf_protect
def login_view(request):
    # Si ya tiene sesión, lo mandamos a su panel
    if _is_logged(request):
        return redirect("admin_home" if _role(request) == "administrador" else "empleado_home")

    ctx = {"error": None}
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        rol_front = request.POST.get("rol", "")
        remember = request.POST.get("remember", "")

        if not email or not password or not rol_front:
            ctx["error"] = "Completa correo, contraseña y rol."
            return render(request, "seguridad/login_empleados.html", ctx)

        rol_db = _map_front_rol(rol_front)
        if not rol_db:
            ctx["error"] = "Rol inválido."
            return render(request, "seguridad/login_empleados.html", ctx)

        try:
            user = Usuarios.objects.select_related("rol").get(
                email=email, rol__nombre=rol_db, estado="activo"
            )
        except Usuarios.DoesNotExist:
            ctx["error"] = "Credenciales incorrectas. Intenta nuevamente."
            return render(request, "seguridad/login_empleados.html", ctx)

        # Soporta hash y texto plano (temporal)
        clave_db = user.clave or ""
        if clave_db.startswith(("pbkdf2_", "argon2$", "bcrypt$")):
            ok = check_password(password, clave_db)
        else:
            ok = (password == clave_db)

        if not ok:
            ctx["error"] = "Credenciales incorrectas. Intenta nuevamente."
            return render(request, "seguridad/login_empleados.html", ctx)

        # Login OK: guardamos mínimos en sesión
        request.session["usuario_id"] = user.id
        request.session["usuario_email"] = user.email
        request.session["rol"] = user.rol.nombre  # "administrador" | "empleado"
        # 14 días si marcó "Recordar sesión"
        request.session.set_expiry(60 * 60 * 24 * 14 if remember == "on" else 0)

        return redirect("admin_home" if user.rol.nombre == "administrador" else "empleado_home")

    return render(request, "seguridad/login_empleados.html", ctx)


def logout_view(request):
    """
    Versión corta por compatibilidad, si la estabas usando.
    """
    return cerrar_sesion(request)


# ---------- Paneles ----------
@require_role("administrador")
def admin_home(request):
    try:
        current_user = Usuarios.objects.select_related("rol").get(
            id=request.session.get("usuario_id")
        )
    except Usuarios.DoesNotExist:
        return redirect("logout")

    total_libros = Libros.objects.count()
    empleados_activos = Usuarios.objects.filter(
        rol__nombre="empleado", estado="activo"
    ).count()
    hoy = timezone.localdate()
    alertas = Prestamos.objects.filter(
        fecha_devolucion__isnull=True, fecha_fin__lt=hoy
    ).count()
    empleados = Usuarios.objects.select_related("rol").filter(
        rol__nombre="empleado"
    ).order_by("id")

    ctx = {
        "current_user": current_user,
        "total_libros": total_libros,
        "ventas_mensuales": None,  # aún no hay tabla de ventas
        "empleados_activos": empleados_activos,
        "alertas": alertas,
        "empleados": empleados,
    }
    return render(request, "seguridad/admin_home.html", ctx)


@require_role("empleado")
def empleado_home(request):
    return render(request, "seguridad/empleado_home.html")


# ---------- Alta de empleados ----------
@require_role("administrador")
@csrf_protect
def crear_empleado(request):
    """
    Crea usuarios con rol 'administrador' o 'empleado'.
    """
    ctx = {"ok": None, "error": None}

    if request.method == "POST":
        nombre_completo = request.POST.get("nombre", "").strip()
        email = request.POST.get("email", "").strip()
        clave = request.POST.get("clave", "")
        rol_front = request.POST.get("rol", "")
        estado = request.POST.get("estado", "activo")

        if not (nombre_completo and email and clave and rol_front):
            ctx["error"] = "Completa nombre, email, clave y rol."
            return render(request, "seguridad/registrar_empleados.html", ctx)

        partes = nombre_completo.split()
        nombre = partes[0]
        apellido = " ".join(partes[1:]) if len(partes) > 1 else ""

        rol_db = _map_front_rol(rol_front)
        if rol_db not in ("administrador", "empleado"):
            ctx["error"] = "Rol inválido."
            return render(request, "seguridad/registrar_empleados.html", ctx)

        try:
            rol_obj = Roles.objects.get(nombre=rol_db)
        except Roles.DoesNotExist:
            ctx["error"] = "No existe el rol seleccionado. Crea 'administrador' y 'empleado' en la tabla Roles."
            return render(request, "seguridad/registrar_empleados.html", ctx)

        if Usuarios.objects.filter(email=email).exists():
            ctx["error"] = "Ya existe un usuario con ese correo."
            return render(request, "seguridad/registrar_empleados.html", ctx)

        Usuarios.objects.create(
            rol=rol_obj,
            nombre=nombre,
            apellido=apellido,
            email=email,
            clave=make_password(clave),  # guarda hash
            estado=estado,
        )
        ctx["ok"] = f"Empleado creado: {email}"
        return render(request, "seguridad/registrar_empleados.html", ctx)

    return render(request, "seguridad/registrar_empleados.html", ctx)


# ---------- Compat con nombres usados en urls ----------
def inicio_sesion(request):
    """Alias si alguna plantilla aún llama a 'inicio_sesion'."""
    return render(request, "seguridad/login_empleados.html")


def cerrar_sesion(request):
    """
    Cierra la sesión y limpia cualquier flag custom, luego vuelve al inicio público.
    """
    auth_logout(request)  # Django auth logout
    for key in ("empleado_id", "usuario_id", "current_user_id", "rol", "is_admin", "usuario_email"):
        request.session.pop(key, None)

    # Redirige a la portada pública
    try:
        return redirect("inicio")  # definido en biblio.urls
    except Exception:
        return redirect("/")       # fallback

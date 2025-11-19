import pytest
from biblio.models import Roles, Usuarios
from datetime import datetime

# Nota: Utilizamos @pytest.mark.django_db para asegurar que Pytest
# inicialice la base de datos de pruebas para esta función.

@pytest.mark.django_db
def test_create_user_and_check_foreign_key():
    # 1. ARREGLO: Crear el objeto de llave foránea (Roles)
    # Se debe crear la instancia de Roles primero.
    rol_cliente = Roles.objects.create(
        nombre="Cliente",
        descripcion="Usuario con acceso al catálogo público."
    )

    # 2. ACCIÓN: Crear la instancia de Usuarios
    # IMPORTANTE: Pasamos la INSTANCIA del objeto 'rol_cliente', no un ID.
    usuario = Usuarios.objects.create(
        rol=rol_cliente, # <-- Clave: se pasa el objeto, no un ID.
        nombre="Andrea",
        apellido="Gómez",
        email="andrea.gomez@test.com",
        clave="hashedpassword123", # Claves deben ser siempre largas en Django
        estado="activo",
        # La fecha se puede pasar como un objeto datetime o un string ISO 8601
        fecha_creacion=datetime(2025, 1, 1, 10, 0, 0)
    )

    # 3. ASERCIONES: Verificar que los datos se guardaron correctamente
    
    # Aserción básica de conteo
    assert Usuarios.objects.count() == 1
    
    # Aserción de la llave foránea (la más importante)
    assert usuario.rol.nombre == "Cliente" 
    
    # Aserción de otros campos
    assert usuario.email == "andrea.gomez@test.com"
    assert usuario.estado == "activo"
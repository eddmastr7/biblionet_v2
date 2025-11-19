import pytest
from django.core.management import call_command

# Esta fixture es reconocida por pytest-django.
# Asegura que las migraciones se ejecuten en la base de datos temporal
# antes de que se corra cualquier prueba que use la base de datos.
@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    """
    Función que asegura la creación de tablas y la carga de datos iniciales
    para todas las aplicaciones durante las pruebas.
    """
    with django_db_blocker.unblock():
        # Ejecuta el comando 'migrate' para crear todas las tablas en 
        # la base de datos de pruebas en memoria.
        call_command('migrate') 

        # Si tienes datos iniciales (fixtures) que quieres cargar:
        # call_command('loaddata', 'initial_data.json') # Ejemplo
        pass
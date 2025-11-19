import pytest

from catalogo.models import Libro

@pytest.mark.django_db
def test_crear_libro(db):
    libro = Libro.objects.create(
        titulo="Cien Años de Soledad",
        autor="Gabriel García Márquez"
    )
    assert libro.titulo == "Cien Años de Soledad"
    assert libro.autor == "Gabriel García Márquez"
  
@pytest.mark.django_db
def test_filtrar_libros_disponibles(db):
    Libro.objects.create(titulo="Libro 1", autor="Autor 1", disponible=True)
    Libro.objects.create(titulo="Libro 2", autor="Autor 2", disponible=False)
    Libro.objects.create(titulo="Libro 3", autor="Autor 3", disponible=True)

    libros_disponibles = Libro.objects.filter(disponible=True)
    assert libros_disponibles.count() == 2


@pytest.mark.django_db
def test_buscar_libro_por_titulo(db):
    Libro.objects.create(titulo="El Amor en los Tiempos del Cólera", autor="Gabriel García Márquez")
    Libro.objects.create(titulo="La Sombra del Viento", autor="Carlos Ruiz Zafón")

    libro = Libro.objects.filter(titulo__icontains="Amor").first()
    assert libro is not None
    assert libro.titulo == "El Amor en los Tiempos del Cólera"

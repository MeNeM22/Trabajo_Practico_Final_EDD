"""
Tests para el módulo de APIs.
"""

import pytest
import os
import requests
from src.api.api_open_alex import URL_OPENALEX, buscar_articulos_openalex, extraer_metadatos, guardar_en_csv


def test_openalex_connection():
    """
    Test de conexión a OpenAlex API.
    """
    response = requests.get(URL_OPENALEX)
    assert response.status_code == 200, "No se pudo conectar a OpenAlex API"

def test_thelens_connection():
    """
    Test de conexión a The Lens API.s
    """
    # TODO: Implementar test
    assert True, "Test no implementado"


def test_extract_article_metadata():
    """
    Test de extracción de metadatos de artículos.
    """
    articulos = buscar_articulos_openalex(1, "machine learning")
    meta = extraer_metadatos(articulos)
    articulo = meta[0]

    # ID
    assert isinstance(articulo["id"], str)
    assert articulo["id"].startswith("W")

    # Título
    assert isinstance(articulo["titulo"], str)
    assert len(articulo["titulo"]) > 0

    # Autores
    assert isinstance(articulo["autores"], list)

    # Fecha
    assert isinstance(articulo["fecha_de_publicacion"], str)

    # Resumen (puede ser vacío)
    assert isinstance(articulo["resumen"], str)

    # Tipo
    assert isinstance(articulo["tipo"], str)

    # País de publicación (puede ser None o set)
    assert articulo["pais_de_publicacion"] is None or isinstance(articulo["pais_de_publicacion"], set)

    # Campos de estudio (lista vacía o con elementos)
    assert isinstance(articulo["campos_de_estudio"], list)

    # Palabras clave
    assert isinstance(articulo["palabras_clave"], list)

    # Instituciones del autor (puede ser None)
    assert articulo["institucion_del_autor"] is None or isinstance(articulo["institucion_del_autor"], str)
    assert articulo["id_institucion"] is None or isinstance(articulo["id_institucion"], str)

def test_extract_patent_metadata():
    """
    Test de extracción de metadatos de patentes.
    """
    # TODO: Implementar test
    assert True, "Test no implementado"


def test_save_to_csv():
    """
    Test de guardado de datos en CSV.
    """
    articulos = buscar_articulos_openalex(1, "machine learning")
    meta_datos = extraer_metadatos(articulos)
    ruta_archivo = "data/articulos.csv"
    guardar_en_csv(meta_datos, ruta_archivo)
    assert os.path.exists(ruta_archivo), "El archivo CSV no fue creado"

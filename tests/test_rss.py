
import pytest
import src.rss.lector as l
import os
import feedparser
import csv
# Se cambia test debido a falla de WTO
def test_bbc_rss_feed():
    url_bbc = "https://feeds.bbci.co.uk/news/rss.xml"
    nombre_sitio = "BBC"
    
    noticias = l.leer_rss(url_bbc,nombre_sitio)

    assert len(noticias)>0


def test_elpais_rss_feed():
    noticias = []
    url = "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada"
    nombre_sitio = "El pais"
    noticias = l.leer_rss(url,nombre_sitio)
    
    assert len(noticias)>0


def test_parse_news_item():
   
    ruta_data = os.path.join(os.getcwd(),"data")
    csv_noticias = os.path.join(ruta_data,"noticias.csv")
    txt_visitadas = os.path.join(ruta_data,"visitadas.txt")
    if os.path.exists(csv_noticias) and os.path.exists(txt_visitadas):
        os.remove(csv_noticias)
        os.remove(txt_visitadas) # Elimino los archivos ya creados 


    if not os.path.exists(csv_noticias) and not os.path.exists(txt_visitadas):
        noticias = []
        url = "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada"
        nombre_sitio = "El pais"
        noticias = l.leer_rss(url,nombre_sitio)
        assert len(noticias)>0 # evaluo que sea una lista y no este vacia
        noticia = noticias[0]
        claves_esperadas = {"id","titulo","descripcion","fecha_publicacion","paises_relacionados"}
        assert claves_esperadas.issubset(noticia.keys()), f"Faltan claves en la noticia {noticia.keys()}" #evaluo  si coinciden las claves


def test_extract_country_elpais():
    tags = [{"term":"Portugal"},{ "term":"Alemania"}]
    titulo = "El presidente de Francia visitó Argentina"
    descripcion = "El encuentro entre ambos países fortalece la relación bilateral."
    paises = l.buscar_pais_en_data(tags,titulo,descripcion)
    assert "Francia" in paises and "Argentina" in paises and "Portugal" in paises and "Alemania" in paises, "No se encontro ningun pais"


def test_save_news_to_csv(tmp_path):
    """
    Test de guardado de noticias en CSV.
    """

    #  Preparo la carpeta tmp_path para que luego se borre
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    ruta_csv = data_dir / "noticias.csv"

    #Creo ejemplos de noticias
    noticias = [
        {
            "titulo": "Noticia de prueba",
            "descripcion": "Esta es una descripción de prueba.",
            "fecha_publicacion": "Fri, 08 Nov 2025 10:00:00 GMT",
            "paises_relacionados": {"Argentina", "Chile"},
        }
    ]

   
    cwd_original = os.getcwd()
    os.chdir(tmp_path)  # cambiamos cwd para que use tmp_path/data/
    try:
        l.guardar_csv(noticias, "BBC News") # se guarda en tmp_path. Aunque dentro de guardar_csv, aclaro que es dentro de /data original, al cambiar directorio, se guardar en tmp_path/data/noticias.csv
    finally:
        os.chdir(cwd_original) #cambio al path original

    # --- Verificamos resultados ---
    assert ruta_csv.exists(), "El archivo CSV no fue creado."

    with open(ruta_csv, newline="", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        assert len(reader) == 1, "Debe haber exactamente una noticia guardada."

        fila = reader[0]
        assert fila["Nombre pagina"] == "BBC News"
        assert fila["Titulo"] == "Noticia de prueba"
        assert "Argentina" in fila["Paises relacionados"]
        assert "Chile" in fila["Paises relacionados"]
        assert fila["Fecha de publicacion"].startswith("Fri")
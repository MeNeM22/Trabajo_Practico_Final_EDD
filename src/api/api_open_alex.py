import csv
import os
import requests

URL_OPENALEX = "https://api.openalex.org/works"

# Función para buscar artículos en OpenAlex ingresando el número de resultados por página y el término de búsqueda
def buscar_articulos_openalex(cantidad_por_pagina, termino_busqueda = None):
    params ={
        "per-page": cantidad_por_pagina, 
        "sort": "publication_date:desc" # Ordenar por fecha de publicación descendente
    }
    #Logica para agregar el término de búsqueda si se proporciona
    if termino_busqueda:
        params["search"] = termino_busqueda
    try:
        response = requests.get(URL_OPENALEX, params=params, timeout=10)
        response.raise_for_status()
        articulos = response.json()
        return articulos["results"]
    except requests.RequestException as e:
        return {"error": str(e)}
    
def extraer_datos_de_autores_intitucion(lista):
    lista_de_autores = []
    instituciones_del_autor = []
    for autor in lista:
        try:
            nombre = autor["author"]["display_name"]

            if autor["institutions"] and autor["author_position"] == "first":
                for inst in autor["institutions"]:
                    nombre_instituto = inst["display_name"]
                    id_instituto = inst["id"].rsplit("/")[-1]
                    instituciones_del_autor.append((nombre_instituto,id_instituto))

            lista_de_autores.append(nombre)
        except KeyError as e:
            print(f"Error al extraer datos del autor: {e}")
            continue

    return lista_de_autores, instituciones_del_autor

def extraer_palabras_clave(palabras_clave):
    palabras_encontradas = []
    
    for palabra_clave in palabras_clave:
        try:
            palabra = palabra_clave["display_name"]
            palabras_encontradas.append(palabra)
        except KeyError as e:
           print(f"⚠️ Error al procesar palabra clave: {e}")
           continue
    return palabras_encontradas

def extraer_pais_de_publicacion(articulo):
    try:
        authorships = articulo.get("authorships", [])
        if not authorships:
            return None
        instituciones = authorships[0].get("institutions", [])
        paises = set()
        for institucion in instituciones:
            pais = institucion.get("country_code")
            if pais:
                paises.add(pais)
    except KeyError as e:
        print(f"Error al extraer país de publicación: {e}")
        return None
    except IndexError as e:
        print(f"Error al extraer país de publicación: {e}")
        return None     
    # Devolver los países o None si está vacío
    return paises or None  

def extraer_campos_de_estudio(articulo):
    campos_de_estudio = []
    try:
        topics = articulo.get("topics", [])
        for topic in topics:
            campo = topic.get("display_name")
            if campo:
                campos_de_estudio.append(campo)
    except KeyError as e:
        print(f"Error al extraer campos de estudio: {e}")
    return campos_de_estudio

# Método que calcula la longitud total de los IDs en el índice invertido del resumen, obteniendo el máximo ID en cada lista de IDs
def cantidad_ids_resumen(diccionario):
    longitud_total = 0
    if not diccionario:
        return 0
    longitud_total = max(max(lista_ids) for _ , lista_ids in diccionario.items())
    return longitud_total

def extraer_resumen(articulo):
    indice_invertido = articulo.get("abstract_inverted_index", {})
    longitud_total = cantidad_ids_resumen(indice_invertido)
    lista_tokens = [""] * (longitud_total + 1)
    if not indice_invertido:
        return ""
    for token, lista_ids in indice_invertido.items():
        for id in lista_ids:
            lista_tokens[id] = token
    return " ".join(lista_tokens)

def extraer_metadatos(articulos):
    contenedor = []
    if articulos:
        for articulo in articulos:
            resumen = extraer_resumen(articulo)
            pais_de_publicacion = extraer_pais_de_publicacion(articulo)
            campos_de_estudio = extraer_campos_de_estudio(articulo)
            palabras_clave = extraer_palabras_clave(articulo["keywords"])
            autores, institutos_del_autor = extraer_datos_de_autores_intitucion(articulo["authorships"])
            metadatos = {
                #rsplit va de Der a Iza hasta q encuentra "/" y [-1] devuelve siempre el ultimo elemento
                "id": articulo["id"].rsplit("/")[-1],
                "titulo": articulo["title"],
                "autores":autores,
                "fecha_de_publicacion": articulo["publication_date"],
                "resumen":resumen,
                "tipo": articulo["type"],
                "pais_de_publicacion": pais_de_publicacion,
                "campos_de_estudio": campos_de_estudio,
                "palabras_clave": palabras_clave,
                "institucion_del_autor": institutos_del_autor[0][0] if institutos_del_autor else None,
                "id_institucion":institutos_del_autor[0][1] if institutos_del_autor else None
            }
            contenedor.append(metadatos)  
    return contenedor

def guardar_en_csv(metadatos, nombre_archivo):
    if not metadatos:
        print("No hay metadatos para guardar.")
        return
    try:
        claves = metadatos[0].keys()
        with open(nombre_archivo, 'w', newline='', encoding='utf-8') as f:
            escritor = csv.DictWriter(f, fieldnames=claves)
            escritor.writeheader()
            for dato in metadatos:
                escritor.writerow(dato)
    except FileNotFoundError as e:
        print(f"Archivo no encontrado: {e}")
    except IOError as e:
        print(f"Error al guardar en CSV: {e}")

def mostrar_datos_csv_openalex(): 
    carpeta_actual = os.getcwd()
    ruta_destino = os.path.join(carpeta_actual,"data","articulos.csv") # Obtengo ruta donde se guardara archivo
    archivo_existe = os.path.exists(ruta_destino)

    if not archivo_existe:
        print("No existe ningun archivo, CSV, Consulte las web para almacenar datos")
        return
    with open(ruta_destino,"r",encoding="UTF-8") as f:
        reader = csv.DictReader(f)
        print("*"*50)
        for row in reader:
            print(f"Titulo: {row['titulo']}\n")
            print(f"Id: {row['id']}\n")
            print(f"Autores: {row['autores']}\n")
            print(f"Institucion del autor: {row['institucion_del_autor']}\n")
            print(f"Id institucion: {row['id_institucion']}\n")
            print(f"Fecha de publicacion: {row['fecha_de_publicacion']}\n")
            print(f"Pais/es relacionado/s: {row['pais_de_publicacion']}\n")
            print(f"Resumen: {row['resumen']}\n")
            print(f"Tipo: {row['tipo']}\n")
            print(f"Campos de estudio: {row['campos_de_estudio']}\n")
            print(f"Palabras clave: {row['palabras_clave']}\n")
            print("*"*50)   
        
def consultar_openalex(cantidad_por_pagina, termino_busqueda):
    articulos = buscar_articulos_openalex(cantidad_por_pagina, termino_busqueda)
    if "error" in articulos:
        return articulos
    metadatos = extraer_metadatos(articulos)
    guardar_en_csv(metadatos, "./data/articulos.csv")
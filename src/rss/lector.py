import feedparser
import os
from csv import DictReader,DictWriter
from src.utils.utilidades import *
dict_days = {"Mon": "Lunes",
 "Tue": "Martes",
"Wed": "Miércoles",
"Thur": "Jueves",
"Fri": "Viernes",
"Sat": "Sábado",
"Sun": "Domingo"
 
 }

paises_set = cargar_paises() #Funcion en utilidades


def obtener_dia_semana(fecha_str):
    fecha_español = ""
    possible_date = fecha_str.split(",")
    if possible_date[0] in dict_days:
        dia_espanol = dict_days.get(possible_date[0], "Día desconocido")
        fecha_español = dia_espanol + "," + possible_date[1]

    return fecha_español if fecha_español else fecha_str


 
def buscar_pais_en_data(arreglo, titulo, descripcion):
    paises_relacionados = set()
    paises_lower = {quitar_tildes(pais).lower() for pais in paises_set}

   
    # Revisar los tags del feed
    for registro in arreglo:
        pais_registro = registro["term"]
        pais_registro = quitar_tildes(pais_registro).lower()
        if pais_registro in paises_lower:
            paises_relacionados.add(pais_registro.capitalize())

    # Si no se encontró país en los tags, buscar en título y descripción
 
    for pais in paises_set:
        if pais in titulo or pais in descripcion:
            paises_relacionados.add(pais)



    return paises_relacionados if len(paises_relacionados) > 0 else []


def obtener_id_visitadas():
    ruta = os.path.join(os.getcwd(), "data", "visitadas.txt")
    if not os.path.exists(ruta):
        os.makedirs(os.path.dirname(ruta), exist_ok=True)#Crea rutas para que exista archivo
        open(ruta, "w", encoding="utf-8").close()
        return set()
    with open(ruta, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f.readlines())

def guardar_id_visitada(id_noticia):
    ruta = os.path.join(os.getcwd(), "data", "visitadas.txt")
    with open(ruta, "a", encoding="utf-8") as f:
        f.write(id_noticia + "\n")



def leer_rss(url,nombre_pagina):
    noticias = []
    id_noticias = obtener_id_visitadas() # Lo coloco aca para que en caso de que se borre visitadas.txt en el test, no se cargue antes y se llene con los datos previos.

    try:
        feed = feedparser.parse(url)
    except Exception as e:
        print(f"Error al leer el feed RSS: {e}")
        return []

    for entry in feed.entries:
        tags = getattr(entry, "tags", [])
        id_noticia = str(hash(entry.title + entry.summary)) # Hashea ID segun titulo y descripcion. Si tiene mismo titulo y descripcion, se obtiene el mismo numero

        if id_noticia in id_noticias:
            print("Ya procesada")
            continue  # ya procesada

        noticia = {
            "id": id_noticia,
            "titulo": entry.title,
            "descripcion": entry.summary,
            "fecha_publicacion": entry.published,
            "paises_relacionados": buscar_pais_en_data(tags, entry.title, entry.summary)
        }

        noticias.append(noticia)
        id_noticias.add(id_noticia)
        guardar_id_visitada(id_noticia)

    guardar_csv(noticias,nombre_pagina)
    mostrar_noticias(noticias)
    return noticias



# ---------------- Obtener noticias existentes ----------
def obtener_csv_noticias_existentes():

    carpeta_actual = os.getcwd()
    ruta_destino= os.path.join(carpeta_actual,"data","noticias.csv") # Obtengo ruta donde se guardara archivo
    archivo_existe = os.path.exists(ruta_destino)
    noticias_existentes = list()
    if archivo_existe: #Si existe el archivo lo leo y agrego noticias ya existentes
         with open(ruta_destino,"r",encoding="utf-8") as f:
            reader = DictReader(f)
            for row in reader:
                noticias_existentes.append(row)
    return noticias_existentes


# ---------------- Guardar noticias en CSV ----------------
def guardar_csv(noticias,nombre_pagina):
    carpeta_actual = os.getcwd()
    ruta_destino= os.path.join(carpeta_actual,"data","noticias.csv") # Obtengo ruta donde se guardara archivo
    fieldnames = ["Nombre pagina","Titulo","Descripcion","Fecha de publicacion","Paises relacionados"]
    noticias_existentes = obtener_csv_noticias_existentes() # Obtengo las noticias
            
        # Combinamos las nuevas noticias
    for noticia in noticias:
        paises_string = ",".join(noticia.get("paises_relacionados", [])) if len(noticia.get("paises_relacionados"))>0 else "No hay un pais relacionado" #Separo por comas cada pais, csv, no acepta sets, se convierte a string
        noticias_existentes.append({
            "Nombre pagina":nombre_pagina,
            "Titulo": noticia.get("titulo", ""),
            "Descripcion": noticia.get("descripcion", ""),
            "Fecha de publicacion": noticia.get("fecha_publicacion", ""),
            "Paises relacionados": paises_string
        })
    
        # Escribimos todo el arreglo existente
    with open(ruta_destino, "w", encoding="utf-8", newline="") as f:
        writer = DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(noticias_existentes)





# ---------------- Visualizar CSV completo ----------------
def visualizar_csv_rss():
    carpeta_actual = os.getcwd()
    ruta_destino= os.path.join(carpeta_actual,"data","noticias.csv") # Obtengo ruta donde se guardara archivo
    archivo_existe = os.path.exists(ruta_destino)

    if not archivo_existe:
        print("No existe ningun archivo, CSV, Consulte las web para almacenar datos")
        return
    with open(ruta_destino,"r",encoding="UTF-8") as f:
        reader = DictReader(f)
        print("CSV Generad  o")
        print("*"*50)
        for row in reader:
            print(f"\nNoticia del medio: {row['Nombre pagina']}")
            print("--"*50)
            print(f"Titulo {row['Titulo']}\n")
            print(f"Descripcion {row['Descripcion']}\n")
            print(f"Fecha de publicacion: {row['Fecha de publicacion']}\n")
            print(f"Pais/es relacionado/s: {row['Paises relacionados']}\n")
            print("*"*50)
            



# ---------------- mostrar noticias por consola ----------------
def mostrar_noticias(noticias):
    for noticia in noticias:
        print("\nTítulo: ", noticia["titulo"])
        print("Descripción: ", noticia["descripcion"])
        print("Fecha de Publicación: ", obtener_dia_semana(noticia["fecha_publicacion"]))
        print("Países relacionados: ", noticia["paises_relacionados"])
        print("-" * 50)

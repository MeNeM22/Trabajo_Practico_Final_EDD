import os
import csv

def guardar(dictAGuardar):
    campos = ["scrap_de","nombre_evento","descripcion","fecha",
                  "ubicacion","sector_industrias_relacionadas",
                  "web_oficial","contacto_correo"]
    
    archivo = "data/eventos.csv"

    if not os.path.exists(archivo) or os.path.getsize(archivo) == 0:
        with open (archivo,"w",newline="",encoding="UTF-8") as f:
            writer = csv.DictWriter(f, fieldnames=campos, delimiter=";")
            writer.writeheader()
            writer.writerow(dictAGuardar)

    else:
         with open (archivo,"a",newline="",encoding="UTF-8") as f:
            writer = csv.DictWriter(f, fieldnames=campos, delimiter=";")
            writer.writerow(dictAGuardar)


def enDict(pagina=None,textoNombreEvento=None,textoDescripcionEvento=None,textoFecha=None,textoLugarEvento=None,textoPais=None,textoSectores=None,textoPaginaWeb=None,textoCorreo=None):
    evento = {
        "scrap_de": pagina,
        "nombre_evento": textoNombreEvento,
        "descripcion":textoDescripcionEvento,
        "fecha": textoFecha,
        "ubicacion":f"{textoLugarEvento} en {textoPais}",
        "sector_industrias_relacionadas": textoSectores,
        "web_oficial":textoPaginaWeb,
        "contacto_correo":textoCorreo,
        }
    
    return evento
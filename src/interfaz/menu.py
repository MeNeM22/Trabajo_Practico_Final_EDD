"""
Módulo de menú principal.
Gestiona la interfaz de consola y la navegación del usuario.
"""
import os
import time
from src.api.api_open_alex import consultar_openalex, mostrar_datos_csv_openalex
from src.rss import lector
import src.scraping.eventsEyeScrap as eventsEye
import src.scraping.nferiasScrap as nferias
import src.scraping.tenTimesScrap as tenTimes

def mostrar_menu_principal():
    """
    Muestra el menú principal y gestiona las opciones del usuario.
    """
    while True:
        limpiarTerminal()
        print("\n" + "=" * 70)
        print("\t\t\t   MENÚ PRINCIPAL")
        print("=" * 70)
        print("\n\t\t   Recuperación de Información en la Web")
        print("-" * 70)
        print()
        print("1. Consultar artículos científicos (OpenAlex)")
        print("2. Consultar próximos eventos y ferias (Web Scraping)")
        print("3. Consultar últimas noticias de comercio exterior (RSS)")
        print("4. Ver archivos CSV generados")
        print("5. Acerca de")
        print("6. Salir")
        print()

        opcion = input("Seleccione una opción [1-6]: ").strip()

        if opcion == "1":
            print("\n\t📚 Consulta de artículos científicos en OpenAlex")
            print("-" * 70)
            print("1. Realizar consulta con un tema específico")
            print("2. Realizar consulta general (sin tema específico)")
            
            subopc = input("\nSeleccione una opción [1-2]: ").strip()

            if subopc in ("1", "2"):
                while True:
                    resultados_por_pagina = input("Ingrese cantidad de resultados por página: ").strip()
                    if resultados_por_pagina.isdigit() and int(resultados_por_pagina) > 0:
                        break
                    print("❌ Valor inválido. Ingrese un número entero mayor a 0.\n")

                termino_busqueda = None
                if subopc == "1":
                    termino_busqueda = input("Ingrese el término de búsqueda (opcional): ").strip()
                    termino_busqueda = termino_busqueda if termino_busqueda else None

                consultar_openalex(resultados_por_pagina, termino_busqueda)

                limpiarTerminal()
                print("\n✅ ¡Consulta realizada con éxito!")
                print("📁 Metadatos guardados en: ./data/articulos.csv\n")

            else:
                print("\n❌ Opción inválida. Por favor seleccione 1 o 2.\n")

        elif opcion == "2":
            mostrarMenuScrap()
        elif opcion == "3":
            print("¿De donde prefiere informarse?: ")
            print("1. BBC")
            print("2. El País")
            fuente = input("Seleccione una opción [1-2]: ").strip()
            if fuente == "1":
                lector.leer_rss("https://feeds.bbci.co.uk/news/rss.xml","BBC")
            if fuente == "2":
                lector.leer_rss("https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada","El Pais")
         
        elif opcion == "4":
            limpiarTerminal()
            print("\n\t\t Visualizacion de archivos CSV")
            print("-" * 70)
            while True:
                opcion_csv = input(
                    "\nSeleccione el tipo de archivo CSV a visualizar:\n"
                    "1. Artículos científicos (OpenAlex)\n"
                    "2. Eventos y ferias\n"
                    "3. Noticias RSS\n"
                    "4. Salir\n"
                    "Seleccione una opción [1-4]: "
                ).strip()

                if opcion_csv == "1":
                    print("\n📂 Visualización de archivos API OpenAlex generados")
                    mostrar_datos_csv_openalex()

                elif opcion_csv == "2":
                    if not os.path.exists("data/eventos.csv"):
                        print("\nNo se scrapeo nada aún")
                        time.sleep(2)
                        limpiarTerminal()
                    else:
                        mostrarScrapCSV()

                elif opcion_csv == "3":
                    print("\n📂 Visualización de archivos RSS generados")
                    lector.visualizar_csv_rss()

                elif opcion_csv == "4":
                    confirmar = input("\n¿Está seguro que desea salir? [S/N]: ").strip().upper()

                    if confirmar in ("S", "SI"):
                        limpiarTerminal()
                        print("\n✅ ¡Gracias por usar el sistema de consultas!")
                        print("📚 Documentación disponible en: ./docs/")
                        print("\n¡Hasta luego! 👋\n")
                        break

                    elif confirmar in ("N", "NO"):
                        continue

                    else:
                        print("\n❌ Respuesta inválida. Use S/N.\n")

                else:
                    print("\n❌ Opción inválida. Por favor seleccione un número del 1 al 4.")
        elif opcion == "5":
            mostrar_acerca_de()
        elif opcion == "6":
            confirmar = input("\n¿Está seguro que desea salir? [S/N]: ").strip().upper()
            if confirmar == "S":
                print("\n✅ ¡Gracias por usar el sistema!")
                print("📚 Documentación disponible en: ./docs/")
                print("\n¡Hasta luego! 👋\n")
                break
        else:
            print("\n❌ Opción inválida. Por favor, seleccione una opción del 1 al 6.")

        input("\nPresiona Enter para continuar...")


def mostrar_acerca_de():
    """
    Muestra información sobre el proyecto.
    """
    print("\n" + "=" * 70)
    print("  ACERCA DE")
    print("=" * 70)
    print()
    print("📚 Trabajo Práctico: Recuperación de Información en la Web")
    print()
    print("🎓 Universidad Nacional de Tres de Febrero")
    print("   Licenciatura en Informática")
    print("   Estructuras de Datos y Algoritmos")
    print()
    print("👥 Equipo de Desarrollo:")
    print("   - Menechino. Agustin")
    print("   - Hernandez. Gonzalo ")
    print("   - Luciano Diaz")
    print("   - Jazmin Cabral")
    print()
    print("📅 Fecha: Noviembre 2025")
    print()
    print("🛠️ Tecnologías utilizadas:")
    print("   - Python 3.x")
    print("   - requests (APIs y HTTP)")
    print("   - cloudparser (Web Scraping)")
    print("   - BeautifulSoup (Web Scraping)")
    print("   - feedparser (RSS)")
    print("   - pandas (Manipulación de datos)")
    print()
    print("🌐 Fuentes de datos:")
    print("   - OpenAlex (artículos científicos)")
    print("   - The Lens (patentes)")
    print("   - eventseye.com, nferias.com, 10times.com (eventos)")
    print("   - WTO y UN Comtrade (noticias RSS)")
    print()

def mostrarMenuScrap():
    while True:
        limpiarTerminal()
        print("\n" + "=" * 70)
        print("\t\t\t\tWeb Scraping. \n\t\tRealizado por Luciano Diaz λ y Jazmin Cabral")
        print("=" * 70)
        print("1. Consultar nferias.com")
        print("2. Consultar EventsEyes.com")
        print("3. Consultar 10times.com")
        print("4. Salir")
                
        opcion = input("Seleccione una opción [1-4]: ").strip()

        if opcion == "1":
            menuEleccionCantScrapNferias(scrapearNFerias)
        elif opcion == "2":
            menuEleccionCantScrapEventsEye(scrapearEventsEye)
        elif opcion == "3":
            menuEleccionCantScrap10times(scrapear10times)
        elif opcion == "4":
            confirmar = input("\n¿Está seguro que desea salir? [S/N]: ").strip().upper()
            if confirmar == "S" or confirmar == "SI":
                limpiarTerminal()
                print("\n✅ ¡Gracias por usar el sistema de scrap!")
                print("📚 Documentación disponible en: ./docs/")
                print("\n¡Hasta luego! 👋\n")
                break
            elif confirmar == "N" or confirmar == "NO":
                continue
            else:
                print("\n❌ Opción inválida.")
        else:
           print("\n❌ Opción inválida. Por favor, seleccione una opción del 1 al 4.")
        
        input("\nPresione Enter para continuar...")
        

def menuEleccionCantScrapNferias(func_scrap):
    opcionScrap = input("¿Desea elegir la cantidad de la pagina que será scrapeada? [S/N]: ").strip().upper()

    if opcionScrap == "S":
        limpiarTerminal()
        while True:
            cantidadScrap = input("Solo números, separados por coma. Ejemplo 1,1,1"
            "\nCant. de letras, Sectores por letra, Eventos por sector: ").strip()

            resultado = cantidadScrap.split(sep=",")

            if len(resultado) == 3 and all(r.strip().isdigit() for r in resultado):
                break
            else:
                    print("Error: Debe ingresar exactamente 3 números separados por coma.")

        print("Consultando nferias.com, por favor espere...")
        func_scrap(resultado[0],resultado[1],resultado[2])
    else:
        func_scrap()

def menuEleccionCantScrapEventsEye(func_scrap):
    opcionScrap = input("¿Desea elegir la cantidad de la pagina que será scrapeada? [S/N]: ").strip().upper()

    if opcionScrap == "S":
        limpiarTerminal()
        while True:
            cantidadScrap = input("Solo números, separados por coma. Ejemplo: 1,1"
            "\nCant. de industrias, eventos por industria: ").strip()
            resultado = cantidadScrap.split(sep=",")

            if len(resultado) == 2 and all(r.strip().isdigit() for r in resultado):
                break
            else:
                    print("Error: Debe ingresar exactamente 2 números separados por coma.")

            print("Consultando nferias.com, por favor espere...")

        print("Consultando eventsEye.com, por favor espere...")
        func_scrap(resultado[0],resultado[1])
    else:
        func_scrap()

def menuEleccionCantScrap10times(func_scrap):
    opcionScrap = input("¿Desea elegir la cantidad de la pagina que será scrapeada? [S/N]: ").strip().upper()

    if opcionScrap == "S":
        limpiarTerminal()
        while True:
            cantidadScrap = input("Solo números, separados por coma. Ejemplo 1,1"
            "\nCant. de Eventos, cant. de categorias: ").strip()

            resultado = cantidadScrap.split(sep=",")

            if len(resultado) == 2 and all(r.strip().isdigit() for r in resultado):
                break
            else:
                    print("Error: Debe ingresar exactamente 2 números separados por coma.")

        print("Consultando 10times.com, por favor espere...")
        func_scrap(resultado[0],resultado[1])
    else:
        func_scrap()

def menuContenidoFinalGeneradoScrap(paginaScrapeada):
    limpiarTerminal()
    print("\nArchivo generado en data/eventos.csv 😎")
    print(f"\n✅ ¡Gracias por scrapear {paginaScrapeada}.com!")
    print("\n¡Hasta luego! 👋\n")

def scrapearNFerias(cantLetras=None,cantSectores=None,cantEventos=None):
    if None in (cantLetras, cantSectores, cantEventos):
        nferias.scrap_nferias()
    else:
         nferias.scrap_nferias(int(cantLetras),int(cantSectores),int(cantEventos))  # type: ignore

    menuContenidoFinalGeneradoScrap("nferias")

def scrapearEventsEye(cantLetras=None,cantSectores=None):
    if None in (cantLetras, cantSectores):
        eventsEye.scrape_events_eye()
    else:
        eventsEye.scrape_events_eye(int(cantLetras),int(cantSectores))  # type: ignore

    menuContenidoFinalGeneradoScrap("eventseye")

def scrapear10times(cantEventos=None,cantCategorias=None):
    if None in (cantEventos, cantCategorias):
        tenTimes.scrape10Times()
    else:
        tenTimes.scrape10Times(int(cantEventos),int(cantCategorias)) # type: ignore
    menuContenidoFinalGeneradoScrap("10times")

def limpiarTerminal():
    os.system("cls" if os.name == "nt" else "clear") 

def mostrarScrapCSV():
        limpiarTerminal()
        print("\n📂 Visualización de archivos Web Scraping generados")
        with open("data/eventos.csv","r",encoding="UTF-8") as f:
            eventos = f.readlines()[1:]

        print("\n" + "=" * 110)
        print("\n\t\t\t\t\t\tFORMATO:\nscrap_de;nombre_evento;descripcion;fecha;ubicacion;sector_industrias_relacionadas;web_oficial;contacto_correo")
        print("\n" + "=" * 110)

        for i, resultado in enumerate(eventos):
            print(f"{i +1}: {resultado}\n")

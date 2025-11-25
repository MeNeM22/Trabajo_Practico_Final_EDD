import string
from src.scraping import guardarEventos as guardar
from src.scraping import robots as robots
import re

def scrap_nferias(cantLetras=3,cantSectores=2, cantEventos=17):
    baseURL = "https://www.nferias.com/sectores/"
    headers = "MiCrawlerTP/1.5 (luciano22diaz@gmail.com)"
    
    letras = ["3"] + list(string.ascii_lowercase)

    for i_letra, letra in enumerate(letras):
        
        if i_letra > cantLetras-1:
            break

        startURL = baseURL + letra + "/"
        soup = robots.respectRobots(startURL,headers) #parse de nferias/sectores/3
        
        if not soup:
            print(f"No se puede acceder a la letra {letra}, se salta")
            continue
        evento = soup.select("ul.list-unstyled.sitemap > li > a[href]")
        eventoURL = [a.get("href") for a in evento]


        for i_sector, url_sector  in enumerate(eventoURL): #obtengo 'cantSectores' sectores, dentro de cada letra (A,B,C,etc)
            
            if i_sector > cantSectores-1:
                break
            
            eventos_contados = 0
            
            while True:

                sopa = robots.respectRobots(url_sector,headers)
                
                if not sopa:
                    print(f"No se puede acceder al sector {url_sector}, se salta")
                    continue

                cadaEvento = sopa.select("article.mb-4 > article[data-href]")
                cadaEventoURL = [a.get("data-href") for a in cadaEvento]

                for evento in cadaEventoURL: #obtengo 'cantEventos' de eventos, dentro de cada categoria, listo para scrap
                    
                    if eventos_contados > cantEventos-1:
                        break
                    
                    sopita = robots.respectRobots(evento,headers)
                    
                    if not sopita:
                        print(f"No se puede acceder al evento {evento}, se salta")
                        continue

                    #Extraccion de info de cada evento
                    nombreEvento = sopita.select("header > div > div > div.col-md-10.col-9 > h1.nTitle")
                    textoNombreEvento = nombreEvento[0].get_text(strip=True, separator=" ") if nombreEvento else None
                    
                    descripcionEvento = sopita.select("div.col-md-9 > article:nth-child(1) > p")
                    textoDescripcionEvento = " ".join([a.get_text(strip=True) for a in descripcionEvento])
                    textoDescripcionEvento = re.sub(r"\s+", " ", textoDescripcionEvento).replace("\xa0", " ") if textoDescripcionEvento else None

                    sectoresEvento = sopita.select("div.col-md-9 > article.mb-4 > ul.list-unstyled >li:first-child > a[href]")
                    textoSectores = [a.get_text(strip=True) for a in sectoresEvento] if sectoresEvento else None

                    infoUbicacionYPag = sopita.select("div.col-md-9 > article.mb-4:nth-child(3) > ul.list-unstyled >li > a[href]")
                    textoLugarEvento = infoUbicacionYPag[0].get_text(strip=True, separator=" ")  if len(infoUbicacionYPag) > 0 else None
                    textoPais = ", ".join([a.get_text(strip=True) for a in infoUbicacionYPag[1:3]])   if len(infoUbicacionYPag) > 1 else None
                    textoPaginaWeb = infoUbicacionYPag[3].get_text(strip=True, separator=" ")  if len(infoUbicacionYPag) > 3 else None

                    parrafos = sopita.select("article[data-href] > p, article.mb-4 > p, article > p")  # un selector más genérico
                    textoCorreo = None

                    for p in parrafos:
                        txt = p.get_text(strip=True) 

                        match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", txt) # Busca si tiene un correo
                        if match:
                            textoCorreo = match.group(0)
                            break

                    fecha = sopita.select_one("div.col-md-9 > article.mb-4:nth-child(3) > ul.list-unstyled > li:first-child")
                    textoFecha = fecha.get_text(strip=True, separator=" ") if fecha else None

                    evento = guardar.enDict("nferias",textoNombreEvento,textoDescripcionEvento,textoFecha,textoLugarEvento,textoPais,textoSectores,textoPaginaWeb,textoCorreo)
                    guardar.guardar(evento)
                    print(evento)
                    eventos_contados += 1
                
                botones = sopa.find_all('a', class_='page-link')
                pagina_siguiente = None
                
                if eventos_contados > cantEventos-1:
                    break
                
                for b in botones:
                    if b.get("rel") == ["next"]: #type: ignore
                        pagina_siguiente = b.get("href")  #type: ignore
                        break
                    url_sector = pagina_siguiente
                  
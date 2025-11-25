
from urllib.parse import urljoin
from src.scraping import guardarEventos as guardar
import src.scraping.robots as robots

def scrape_events_eye(limiteIndustrias=3,limiteSectoresIndustria=5):
    baseURL = "https://www.eventseye.com/ferias/"
    startURL = baseURL + "ferias-por-tema.html"

    headers= "MiCrawlerTP/1.5 (luciano22diaz@mail)"
    
    soup = robots.respectRobots(startURL,headers)
    if not soup:
        return
    
    cadaIndustria = soup.find_all("div", class_="body")
    enlaces = []

    for industrias in cadaIndustria:
        enlaces.extend(industrias.find_all("a")) # type: ignore
    
    for idx_industria, industria in enumerate(enlaces): # obtiene 'limiteIndustrias' URL's de las industrias

        if idx_industria > limiteIndustrias-1:
            break

        href = industria.get("href") # type: ignore
        urlStartFeriaIndustriaCompleta = urljoin(baseURL,href) # type: ignore
        urlNextPage = urlStartFeriaIndustriaCompleta.replace(".html", "")
        contador = 0
        ferias_contadas = 0

        while ferias_contadas < limiteSectoresIndustria:
            if contador == 0:
                urlPagina = urlStartFeriaIndustriaCompleta
            else:
                urlPagina = f"{urlNextPage}_{contador}.html"
                
            sopa = robots.respectRobots(urlPagina,headers)
            if not sopa:
                contador+=1
                continue

            ferias = sopa.select("table.tradeshows > tbody > tr > td:nth-child(1) > a[href]")
            hrefs = [a.get("href") for a in ferias] #Todas las ferias de la pagina actual
            
            for index_href, href in enumerate(hrefs): #Extraccion de cada una de las ferias
                if index_href > limiteSectoresIndustria-1:
                    break

                urlFeria = urljoin(baseURL,href) # type: ignore

                sopita = robots.respectRobots(urlFeria,headers)
                if not sopita:
                    continue

                #Extraccion de info de cada feria
                descripcionEvento = sopita.find("div", class_="description")
                textoDescripcion = descripcionEvento.get_text(strip=True, separator=" ") # type: ignore
                textoDescripcion = textoDescripcion.replace("Descripción", "")

                nombreEvento = sopita.select("div.title-line > div:nth-child(2)")
                textoEvento = ", ".join([a.get_text(strip=True) for a in nombreEvento])

                paisEvento = sopita.select("table.dates > tbody > tr > td:nth-child(2) > a")
                textoPais = ", ".join([a.get_text(strip=True) for a in paisEvento])

                fechaEvento = sopita.select("table.dates > tbody > tr > td:nth-child(1)")
                textoFecha = ", ".join([a.get_text(strip=True) for a in fechaEvento])

                lugarEvento = sopita.select("table.dates > tbody > tr > td:nth-child(3)")
                textoLugar = ", ".join([a.get_text(strip=True) for a in lugarEvento])

                correoYSitio = sopita.select("div.more-info > a[href]")
                textoSitio = correoYSitio[0].get("href")
                textoCorreo = correoYSitio[1].get("href").replace("mailto:", "") # type: ignore

                industriasRelacionadas = sopita.select("div.drac-group > div.industries > a")
                textoindustriasRelacionadas = ", ".join([a.get_text(strip=True) for a in industriasRelacionadas])
                        
                feria = guardar.enDict("eventseye",textoEvento,textoDescripcion,textoFecha,textoLugar,textoPais,textoindustriasRelacionadas,textoSitio,textoCorreo)
                guardar.guardar(feria)
                ferias_contadas+=1
            contador+=1

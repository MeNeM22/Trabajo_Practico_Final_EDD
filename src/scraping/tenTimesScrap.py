import cloudscraper
import re
from bs4 import BeautifulSoup
from src.scraping import guardarEventos as guardar

def scrape10Times(cantEventos=1, cantCategorias=2):
    baseURL = "https://10times.com"
   
    #lista con las categorias
    categorias = hacerRequest(baseURL)
    sopa = BeautifulSoup(categorias,"lxml") #type: ignore
    elementos = sopa.find_all('a', class_='bg-white')
    
    contador_categoria = 0
    
    for elemento in elementos:
        
        if contador_categoria >= cantCategorias:
           break
        
        #obtengo la categoria
        categoria = elemento.get("href") #type: ignore
        
        #entro en la categoria
        eventos = hacerRequest(baseURL +"/"+ f"{categoria}")
        sopita = BeautifulSoup(eventos,"lxml") #type: ignore
        
        #lista de eventos
        elementos2 = sopita.find_all('td', class_='col-12 c-ga cursor-pointer text-break show-related')
        contador_eventos = 0
        
        for element in elementos2:
           
            if contador_eventos >= cantEventos:
                break
            
            #obtengo el evento
            encontrar_url_evento = element.get("onclick") #type: ignore
                            
            #limpiar url
            match = re.search(r"window\.open\('([^']+)'\)", encontrar_url_evento) #type: ignore
            url_evento = match.group(1)
            
            #entro al evento
            evento = hacerRequest(url_evento)
            soup = BeautifulSoup(evento,"lxml") #type: ignore
            
            #=====================================Extraccion de datos============================================#
                        
            #obtener nombre del evento
            encontrar_nombre = soup.select_one("div.col-md-8 h1")
            nombre_del_evento = encontrar_nombre.get_text(strip=True) if encontrar_nombre else ""
            
            #obtener lugar del evento
            encontrar_lugar = soup.find_all('a', class_='text-muted')

            for k, elem in enumerate(encontrar_lugar):
                if k == 1:
                    ciudad = elem.text
                else:
                    pais = elem.text
                            
            #obtener descripcion del evento
            encontrar_descripcion = soup.find('span', id='paragraph', class_=False)
            encontrar_descripcion2 = soup.find('span', id='more_content_desc')
            
            match2 = re.search(r"(.+)\.\.\.Read More", encontrar_descripcion.get_text(strip=True)) #type: ignore
            
            descripcion = match2.group(1) if match2 else encontrar_descripcion.get_text(strip=True) #type: ignore
            
            if encontrar_descripcion2:
                descripcion += " " + encontrar_descripcion2.get_text(strip=True)
                            
            # obtener fecha del evento
            encontrar_fecha = soup.find('span', attrs={"content": re.compile(r"\d{4}-\d{2}-\d{2}"), "data-localizer":"ignore"})
            fecha = encontrar_fecha.text #type: ignore
            
            #obtener sector
            encontrar_sector = soup.find_all('a', class_='text-decoration-none text-muted-new',attrs={"target":"_blank"})
            sectores = ""
            for sector in encontrar_sector:
                if not sector.get_text(strip=True).startswith('#'):
                    sectores += sector.get_text(strip=True)
                            
            #obtener web oficial
            #obtener correo de 
            
            evento = guardar.enDict("10Times", nombre_del_evento, descripcion, fecha, ciudad, pais, sectores)
            guardar.guardar(evento)
            
            contador_eventos += 1
        contador_categoria += 1
    
def hacerRequest(url):
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url)
        return response.text
    except Exception as e:
        print(f"❌ Failed - {str(e)}")
    
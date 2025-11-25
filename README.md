# 🧠 Recuperación de Información en la Web – Proyecto Grupal

Este repositorio reúne el desarrollo del trabajo práctico de la materia **Recuperación de Información en la Web**, donde implementamos un sistema completo en Python para obtener, procesar y almacenar datos provenientes de **APIs**, **Web Scraping** y **feeds RSS**.  
Además, incluye un informe en Jupyter Notebook y una interfaz por consola para consultar los resultados.

---

## 📌 Resumen del Proyecto

### **1️⃣ APIs – Artículos científicos (OpenAlex)**  
Implementamos consultas a la API de **OpenAlex**, obteniendo y procesando:

- ID del artículo  
- Título  
- Autores e institución  
- Fecha y año de publicación  
- Resumen (reconstruido desde índice invertido)  
- Tipo de publicación  
- País relacionado  
- Campos de estudio  
- Palabras clave  

Los datos procesados se guardan en `data/articulos.csv`.

---

### **2️⃣ Web Scraping – Eventos y Ferias**  
Mediante scrapers sobre Eventseye, Nferias y 10Times extraemos:

- Nombre del evento  
- Descripción  
- Fecha  
- Ubicación  
- Sector / industria  
- Web oficial  
- Contacto  

Resultado consolidado en `data/eventos.csv`.

---

### **3️⃣ RSS – Noticias de Comercio Internacional**  
Procesamos feeds RSS de:

- Organización Mundial del Comercio (WTO)  
- UN Comtrade  

Extrayendo:

- Título  
- Fecha  
- Resumen  
- País asociado  

Guardados en `data/noticias.csv`.

---

## 🖥️ Interfaz por Consola

Incluye un menú que permite:

- Consultar artículos  
- Consultar patentes  
- Consultar eventos  
- Consultar noticias  
- Visualizar archivos CSV existentes  

Todo desde la terminal.

---

## 🧰 Tecnologías Utilizadas

- Python  
- requests  
- BeautifulSoup4  
- feedparser  
- csv  
- pandas  

---

## 📘 Informe

Incluye análisis de:

- Técnicas utilizadas (APIs, scraping, RSS)  
- Diseño y modularización  
- Estructuras de datos  
- Manejo de errores  
- CSV generados  
- Conclusiones y aprendizajes  




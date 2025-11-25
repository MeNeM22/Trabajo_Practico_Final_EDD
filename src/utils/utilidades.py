
import unicodedata

def cargar_paises():
    paises = ["Argentina", "Brasil", "Chile", "Colombia", "Mexico", "Peru", "Uruguay", "Venezuela", "Ecuador", "Paraguay", "Bolivia", "Guyana", "Surinam", "Panama", "Costa Rica", "Cuba", "Republica Dominicana", "Honduras", "El Salvador", "Nicaragua", "Guatemala","Israel","España","Estados Unidos","Francia","Alemania","Italia","Reino Unido","Francia","Canada","China","Australia","Japon","India","Rusia","Ucrania","Turquia","Sudafrica","Portugal"]
    return set(paises)

# PASAR FUNCION A UTILIDADES
def quitar_tildes(cadena):
    # Normaliza la cadena a forma NFD (Canonical Decomposition)
    # y quita los caracteres que son "Mark, Nonspacing"
    s = ''.join((c for c in unicodedata.normalize('NFD', cadena) if unicodedata.category(c) != 'Mn'))
    return s

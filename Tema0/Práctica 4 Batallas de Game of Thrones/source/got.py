import csv
from collections import namedtuple

# Definición de la namedtuple según el enunciado
BatallaGOT = namedtuple('BatallaGOT', [
    'nombre', 
    'rey_atacante', 
    'rey_atacado', 
    'gana_atacante', 
    'muertes_principales', 
    'comandantes_atacantes', 
    'comandantes_atacados', 
    'region', 
    'num_atacantes', 
    'num_atacados'
])

# ----------------------------------------------------------------------
# Funciones Auxiliares
# ----------------------------------------------------------------------

def parsea_comandantes(cadena):
    """Convierte una cadena separada por comas en una lista de cadenas limpias."""
    cadena = cadena.strip()
    if not cadena:
        return []
    return [c.strip() for c in cadena.split(",")]

def parsea_int_opcional(cadena):
    """Convierte una cadena a int o devuelve None si está vacía."""
    cadena = cadena.strip()
    return int(cadena) if cadena else None


# ----------------------------------------------------------------------
# Ejercicio 1: Lectura del fichero
# ----------------------------------------------------------------------
# Implementa lee_batallas(fichero). Debe abrir un fichero CSV en UTF-8, ignorar la cabecera y
# devolver una lista de objetos BatallaGOT. Convierte "win"/"loss" a bool, "1"/"0" a bool, los
# comandantes a listas y los tamaños de ejército vacíos a None.

def lee_batallas(fichero):
    batallas = []
    with open(fichero, 'r', encoding='utf-8') as f:
        lector = csv.reader(f, delimiter=';')
        next(lector)  # Ignorar la cabecera
        
        for linea in lector:
            nombre = linea[0].strip()
            rey_atacante = linea[1].strip()
            rey_atacado = linea[2].strip()
            
            # Conversión a booleanos
            gana_atacante = linea[3].strip().lower() == 'win'
            muertes_principales = linea[4].strip() == '1'
            
            # Listas de comandantes
            comandantes_atacantes = parsea_comandantes(linea[5])
            comandantes_atacados = parsea_comandantes(linea[6])
            
            region = linea[7].strip()
            
            # Enteros opcionales (o None)
            num_atacantes = parsea_int_opcional(linea[8])
            num_atacados = parsea_int_opcional(linea[9])
            
            b = BatallaGOT(
                nombre, rey_atacante, rey_atacado, gana_atacante,
                muertes_principales, comandantes_atacantes, comandantes_atacados,
                region, num_atacantes, num_atacados
            )
            batallas.append(b)
            
    return batallas


# ----------------------------------------------------------------------
# Ejercicio 2: Reyes con mayor y menor ejército
# ----------------------------------------------------------------------
# Implementa reyes_mayor_menor_ejercito(batallas). Debe devolver una tupla con los nombres
# de los reyes con el mayor y el menor ejército acumulado, respectivamente. Para cada rey se
# suman los soldados de todas las batallas en las que aparece como atacante o como atacado.
# Los valores None no se suman.

def reyes_mayor_menor_ejercito(batallas):
    acumulado = {}
    
    for b in batallas:
        # Sumar al rey atacante
        if b.num_atacantes is not None:
            acumulado[b.rey_atacante] = acumulado.get(b.rey_atacante, 0) + b.num_atacantes
            
        # Sumar al rey atacado
        if b.num_atacados is not None:
            acumulado[b.rey_atacado] = acumulado.get(b.rey_atacado, 0) + b.num_atacados

    rey_mayor = max(acumulado, key=acumulado.get)
    rey_menor = min(acumulado, key=acumulado.get)
    
    return rey_mayor, rey_menor


# ----------------------------------------------------------------------
# Ejercicio 3: Batallas con más comandantes
# ----------------------------------------------------------------------
# Implementa batallas_mas_comandantes(batallas, regiones=None, n=None). Debe devolver
# una lista de tuplas (nombre_batalla, total_comandantes), ordenada de mayor a menor número
# total de comandantes. Si regiones es None se consideran todas las regiones. Si n es None se
# devuelven todas las batallas seleccionadas.

def batallas_mas_comandantes(batallas, regiones=None, n=None):
    # Filtrar por regiones si se indica un conjunto/lista
    if regiones is not None:
        batallas = [b for b in batallas if b.region in regiones]
        
    # Crear tuplas (nombre, total_comandantes)
    resultado = [
            (b.nombre, len(b.comandantes_atacantes) + len(b.comandantes_atacados))
            for b in batallas
    ]
    
    # Ordenar de mayor a menor según el número de comandantes
    resultado.sort(key=lambda t: t[1], reverse=True)
    
    # Recortar si se pasa un n
    if n is not None:
        resultado = resultado[:n]
        
    return resultado


# ----------------------------------------------------------------------
# Ejercicio 4: Rey con más victorias
# ----------------------------------------------------------------------
# Implementa rey_mas_victorias(batallas, rol='ambos'). Si rol es 'atacante', cuenta únicamente
# victorias como atacante; si es 'atacado', únicamente victorias como atacado; y si es 'ambos',
# suma ambas. Si no existe ninguna victoria para el rol indicado, devuelve None.

def rey_mas_victorias(batallas, rol='ambos'):
    victorias = {}
    
    for b in batallas:
        # Victoria del atacante
        if b.gana_atacante and rol in ('atacante', 'ambos'):
            victorias[b.rey_atacante] = victorias.get(b.rey_atacante, 0) + 1
            
        # Victoria del atacado
        elif not b.gana_atacante and rol in ('atacado', 'ambos'):
            victorias[b.rey_atacado] = victorias.get(b.rey_atacado, 0) + 1

    if not victorias:
        return None
        
    return max(victorias, key=victorias.get)


# ----------------------------------------------------------------------
# Ejercicio 5: Rey con más victorias por región
# ----------------------------------------------------------------------
# Implementa rey_mas_victorias_por_region(batallas, rol='ambos'). Debe devolver un
# diccionario que relacione cada región con el rey que acumula más victorias en esa región. El
# parámetro rol tiene el mismo significado que en el ejercicio anterior. Si en una región no hay
# ninguna victoria para el rol indicado, el valor asociado debe ser None. Puedes reutilizar
# rey_mas_victorias.

def rey_mas_victorias_por_region(batallas, rol='ambos'):
    # Extraer todas las regiones únicas
    regiones = {b.region for b in batallas}
    dicc = {}
    
    for reg in regiones:
        # Filtrar batallas asociadas a esa región concreta
        batallas_reg = [b for b in batallas if b.region == reg]
        # Reutilizar la función del Ejercicio 4
        dicc[reg] = rey_mas_victorias(batallas_reg, rol)
        
    return dicc
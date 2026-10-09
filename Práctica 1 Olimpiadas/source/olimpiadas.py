import csv
from collections import namedtuple
Atleta = namedtuple('Atleta', 'nombre, edad, pais, peso')
#pepe, 20, italia, 87.3
def leer_fichero(nombre_fichero):
    registros=[]
    with open(nombre_fichero, encoding='utf-8') as f:
        lector=csv.reader(f)
        next(lector) #esto se salta la primera línea
        for linea in lector:
            nombre=linea[0]
            edad=int(linea[1])
            pais=linea[2]
            peso=float(linea[3])
            tupla=Atleta(nombre, edad, pais, peso)
            registros.append(tupla)
    return registros


#Implementa edad_media(registros). Debe devolver la edad media de todos los atletas.

def edad_media(registros):
    res = 0.0
    for r in registros:
        res+=r.edad
    return res/len(registros)

#Ejercicio 3 · Número de atletas por país 
#Implementa num_atletas_por_pais(registros). Debe devolver un diccionario cuyas claves sean 
#los países y cuyos valores indiquen cuántos atletas pertenecen a cada país.

def num_atletas_por_pais(registros):
    diccionario = {}
    for atleta in registros:
        clave = atleta.pais 
        if clave in diccionario:
            diccionario[clave] += 1
        else: 
            diccionario[clave] = 1
    return diccionario

#Ejercicio 4 · Nombres de atletas por país 
#Implementa nombre_atletas_por_pais(registros). Debe devolver un diccionario cuyas claves 
#sean los países y cuyos valores sean listas con los nombres de los atletas de cada país.

def nombre_atletas_por_pais(registros):
    diccionario = {}
    for atleta in registros:
        clave = atleta.pais
        if clave not in diccionario:
            diccionario[clave] = []
        diccionario[clave].append(atleta.nombre)
    return diccionario

#Ejercicio 5 · Atleta de mayor peso 
#Implementa atleta_mayor_peso(registros). Debe devolver el nombre del atleta con mayor peso. 
def atleta_mayor_peso(registros):
    if not registros:
        return None
    return max(registros, key=lambda atleta: atleta.peso).nombre

#Ejercicio 6 · País con mayor peso medio 
#Implementa pais_mayor_peso_medio(registros). Debe calcular el peso medio de los atletas de 
#cada país y devolver el nombre del país cuyo peso medio sea mayor.
from collections import defaultdict

def pais_mayor_peso_medio(registros):
    if not registros:
        return None

    atletas_por_pais = defaultdict(list)
    for atleta in registros:
        atletas_por_pais[atleta.pais].append(atleta)

    return max(atletas_por_pais,key=lambda pais: sum(a.peso for a in atletas_por_pais[pais]) / len(atletas_por_pais[pais]))

#Ejercicio 7 · Mayor diferencia de edad 
#Implementa metodozip(registros). Ordena los atletas por edad, calcula la diferencia de edad 
#entre cada pareja de atletas consecutivos en esa ordenación y devuelve la mayor de esas 
#diferencias. Debes utilizar zip para emparejar elementos consecutivos.
def metodozip(registros: list) -> int:
    if len(registros) < 2:
        return 0 
    registros_ordenados = sorted(registros, key=lambda t: t.edad)
    lis = []
    for a, b in zip(registros_ordenados, registros_ordenados[1:]):
        lis.append(b.edad - a.edad)
    return max(lis)
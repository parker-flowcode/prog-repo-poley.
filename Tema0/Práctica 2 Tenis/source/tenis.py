import csv
from collections import namedtuple
from datetime import datetime
Partido = namedtuple('Partido', 'fecha, rival, superficie, duracion, juegos_ganados, juegos_perdidos, ganado')
def leer_fichero(nombre_fichero):
    partidos=[]
    with open(nombre_fichero, encoding='utf-8') as f:
        lector=csv.reader(f)
        next(lector) #esto se salta la primera línea
        for linea in lector:
            fecha=datetime.strptime(linea[0], '%d/%m/%Y').date()
            rival=(linea[1])
            superficie=linea[2]
            duracion=int(linea[3])
            juegos_ganados=int(linea[4])
            juegos_perdidos=int(linea[5])
            ganado = False
            if linea[6]=='True':
                ganado = True
            tupla=Partido(fecha, rival, superficie, duracion, juegos_ganados, juegos_perdidos, ganado)
            partidos.append(tupla)
    return partidos

#Ejercicio 1 
#Implementa desviaciones_media(partidos, n). Debe devolver una lista de tuplas (desviacion, 
#partido) con los partidos cuya duración supere en n o más minutos la duración media de todos 
#los partidos. No se pueden usar bucles explícitos. 
#Ejemplo de interpretación 
#Si la duración media es 120 minutos y un partido dura 150, su desviación es 30. Para n=20 ese 
#partido debe aparecer en el resultado. 
def desviaciones_media(partidos, n):
    if not partidos:
        return []
    minutos = [p.duracion for p in partidos]
    media = sum(minutos) / len(minutos)
    return [(d, p) for p in partidos if (d:= p.duracion - media) >= n]


#Ejercicio 2
#Implementa diccionario_diferencia_juegos_superficie(partidos, n=3). Debe devolver un
#diccionario que relacione cada superficie con las fechas de los n partidos jugados en esa
#superficie con mayor diferencia entre juegos ganados y juegos perdidos, ordenados de mayor a
#menor diferencia. Utiliza al menos una función auxiliar.
#Ejemplo de interpretación
#Para una superficie, los partidos con diferencias 8, 6 y 3 deben aparecer antes que uno con
#diferencia 1.
def auxiliar(lista, n):
    lista = sorted(lista, reverse=True, key=lambda t:t.juegos_ganados - t.juegos_perdidos)
    lista = lista[:n]
    return [p.fecha for p in lista]

def diccionario_diferencia_juegos_superficie(partidos, n=3):
    d1 = {}
    for p in partidos:
        clave = p.superficie
        if clave in d1:
            d1[clave].append(p)
        else:
            d1[clave] = [p]
        
    d2 = {}
    for superficie, lista in d1.items():
        d2[superficie] = auxiliar(lista, n)
    return d2


#Ejercicio 3
#Implementa rival_mayor_porcentaje_victorias(partidos, superficie). Debe devolver una tupla
#(rival, porcentaje) con el rival frente al que se haya obtenido el mayor porcentaje de victorias en
#la superficie indicada.
#Ejemplo de interpretación
#Si frente a un rival se han ganado 7 de 10 partidos en tierra, su porcentaje de victorias es 70.0.

def rival_mayor_porcentaje_victorias(partidos, superficie):
    d1 = {}
    for p in partidos: 
            if p.superficie == superficie:
                rival = p.rival
                if rival in d1:
                    d1[rival].append(p)
                else:
                    d1[rival] = [p]

    d2 = {}
    for rival, lista in d1.items():
        d2[rival] = sum(p.ganado for p in lista) / len(lista) * 100
    return max(d2.items(), key=lambda t: t[1])

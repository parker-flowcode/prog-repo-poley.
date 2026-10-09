import csv
from collections import namedtuple
Partido = namedtuple('Partido', 'fecha, rival, superficie, duracion, juegos_ganados, juegos_perdidos, ganado')
def leer_fichero(nombre_fichero):
    partidos=[]
    with open(nombre_fichero, encoding='utf-8') as f:
        lector=csv.reader(f)
        next(lector) #esto se salta la primera línea
        for linea in lector:
            fecha=linea[0]
            rival=(linea[1])
            superficie=linea[2]
            duracion=int(linea[3])
            juegos_ganados=int(linea[4])
            juegos_perdidos=int(linea[5])
            ganado=bool(linea[6])
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
def desviaciones_media(partidos: list, n: int) -> list:
    if not partidos:
        return []
    media = sum(partido.duracion for partido in partidos) / len(partidos)
    return [
        (partido.duracion - media, partido)
        for partido in partidos
        if (partido.duracion - media) >= n
    ]

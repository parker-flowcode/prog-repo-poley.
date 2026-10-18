from tenis import * 
from pathlib import Path

partidos = leer_fichero('./Práctica 2 Tenis/data/datos.txt')

def test_lee_fichero(partidos):
    print()
    print("Test de la función lee fichero")
    print('\tLeidos: ', len(partidos), 'partidos')
    print('\tMostrando los tres primeros')
    for r in partidos[:3]:
        print('\t', r, sep='')

def test_diccionario_diferencia_juegos_superficie(partidos):
    print()
    print('Test diccionario_diferencia_juegos_superficie')
    d=diccionario_diferencia_juegos_superficie(partidos, n=3)
    for clave in d:
        print(clave, ': ', d[clave])
    print()

if __name__=="__main__":
    print("Proyecto Tenis")
    test_lee_fichero(partidos)
    print()
    print('***************************')
    print(desviaciones_media(partidos,5))
    print()
    print('***************************')
    #print( diccionario_diferencia_juegos_superficie(partidos,3) )
    test_diccionario_diferencia_juegos_superficie(partidos)
    print()
    print('***************************')
    print(rival_mayor_porcentaje_victorias(partidos, 'Tierra'))



from tenis import * 
from pathlib import Path

RUTA_PARTIDOS = Path(__file__).parent.parent / 'data' / 'datos.txt'

def test_lee_fichero(partidos):
    print()
    print("Test de la función lee fichero")
    print('\tLeidos: ', len(partidos), 'partidos')
    print('tMostrando los tres primeros')
    for r in partidos[:3]:
        print('\t', r, sep='')

if __name__=="__main__":
    print("Proyecto Tenis")
    partidos=test_lee_fichero(RUTA_PARTIDOS)
    test_lee_fichero(partidos)



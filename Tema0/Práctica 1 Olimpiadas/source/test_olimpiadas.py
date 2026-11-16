from olimpiadas import * 
from pathlib import Path

RUTA_ATLETAS = Path(__file__).parent.parent / 'data' / 'atletas.txt'

def test_lee_fichero(registros):
    print()
    print("test de la función lee_fichero")
    print('\tLeidos: ', len(registros),' registros')
    print('\tMostrando los tres primeros')
    # print(registros[:3])
    for r in registros[:3]:
        print('\t',r, sep='')

if __name__=="__main__":
    print("Proyecto olimpiadas")
    registros=leer_fichero(RUTA_ATLETAS)
    test_lee_fichero(registros)

    print(edad_media(registros))

    print(num_atletas_por_pais(registros))

    print(nombre_atletas_por_pais(registros))

    print(atleta_mayor_peso(registros))

    print(pais_mayor_peso_medio(registros))

    print(metodozip(registros))
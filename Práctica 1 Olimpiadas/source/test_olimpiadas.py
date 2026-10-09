from olimpiadas import * 

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
    registros=leer_fichero('./data/atletas.txt')
    test_lee_fichero(registros)
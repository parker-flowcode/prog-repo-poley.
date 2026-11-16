from got import (
    lee_batallas,
    reyes_mayor_menor_ejercito,
    batallas_mas_comandantes,
    rey_mas_victorias,
    rey_mas_victorias_por_region
)

def ejecutar_pruebas():
    # Asegúrate de ajustar la ruta si guardaste el CSV en una carpeta './data/'
    fichero = './Práctica 4 Batallas de Game of Thrones/data/batallas_practica4.csv' 
    batallas = lee_batallas(fichero)
    
    print("=== TEST EJERCICIO 1: LECTURA DE BATALLAS ===")
    print("Total de batallas leídas:", len(batallas))
    print("\nPrimera batalla [0]:")
    print(" ", batallas[0])
    print("\nÚltima batalla [-1]:")
    print(" ", batallas[-1])
    
    print("\n=== TEST EJERCICIO 2: REYES CON MAYOR Y MENOR EJÉRCITO ===")
    mayor, menor = reyes_mayor_menor_ejercito(batallas)
    print(f"Rey con mayor ejército acumulado: {mayor}")
    print(f"Rey con menor ejército acumulado: {menor}")
    
    print("\n=== TEST EJERCICIO 3: BATALLAS CON MÁS COMANDANTES ===")
    regiones_filtro = {'The North', 'The Riverlands'}
    res_ej3 = batallas_mas_comandantes(batallas, regiones_filtro, 4)
    print("Top 4 batallas en The North y The Riverlands:")
    for nombre, num in res_ej3:
        print(f"  • {nombre}: {num} comandantes")
        
    print("\n=== TEST EJERCICIO 4: REY CON MÁS VICTORIAS ===")
    print("Más victorias (ambos roles):", rey_mas_victorias(batallas))
    print("Más victorias (como atacante):", rey_mas_victorias(batallas, 'atacante'))
    print("Más victorias (como atacado):", rey_mas_victorias(batallas, 'atacado'))
    
    print("\n=== TEST EJERCICIO 5: REY CON MÁS VICTORIAS POR REGIÓN ===")
    print("Por región (ambos roles):")
    for reg, rey in rey_mas_victorias_por_region(batallas).items():
        print(f"  • {reg}: {rey}")
        
    print("\nPor región (rol atacado):")
    for reg, rey in rey_mas_victorias_por_region(batallas, 'atacado').items():
        print(f"  • {reg}: {rey}")

if __name__ == '__main__':
    ejecutar_pruebas()
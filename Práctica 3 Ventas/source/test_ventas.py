from ventas import *

ventas = leer('./Práctica 3 Ventas/data/ventas.txt')

# 1. Lectura
print("=== LECTURA ===")
print("Leídos:", len(ventas), "registros")
for v in ventas[:2]:
    print(" ", v)

# 2. Ejercicio 1 (usamos 'productoA' con 'p' minúscula como viene en el CSV)
print("\n=== EJERCICIO 1: Clientes ===")
print("Clientes:", clientes_producto1_y_producto2(ventas, 'productoA', 'productoC'))

# 3. Ejercicio 2 (redondeamos los porcentajes a 2 decimales para que no salgan 10 dígitos)
print("\n=== EJERCICIO 2: Porcentajes ===")
porcentajes = diccionario_porcentaje_cantidad_producto(ventas)
for prod, pct in porcentajes.items():
    print(f"  {prod}: {pct:.2f}%")

# 4. Ejercicio 3
print("\n=== EJERCICIO 3: Producto más vendido ===")
nombres = {'ClienteA', 'ClienteB'}
print("Producto:", producto_mas_vendido(ventas, nombres, 3))
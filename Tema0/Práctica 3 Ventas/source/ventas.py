from collections import namedtuple
import csv
from datetime import date, datetime

Venta = namedtuple('Venta', 'id, fecha, cliente, producto, cantidad, precio, beneficio')

#2051, 04/06/2019, ClienteB, productoC, 11, 7.60, 2.67
def leer(nombre):
    ventas = []
    with open(nombre, 'r', encoding='utf-8') as f:
        lector =csv.reader(f)
        next(lector) # saltar la cabecera
        for linea in lector:
            id = linea[0].strip()
            fecha = datetime.strptime(linea[1].strip(), '%d/%m/%Y').date()
            cliente = linea[2].strip()
            producto = linea[3].strip()
            cantidad = int(linea[4].strip())
            precio = float(linea[5].strip())
            beneficio = float(linea[6].strip())
            tupla = Venta(id, fecha, cliente, producto, cantidad, precio, beneficio)
            ventas.append(tupla)
    return ventas

# Ejercicio 1
# Implementa clientes_producto1_y_producto2(ventas, producto1, producto2). Recibe una lista de
# objetos Venta y los nombres de dos productos. Debe devolver un conjunto con los nombres de
# los clientes que hayan comprado ambos productos. No se pueden usar bucles explícitos; si
# necesitas iterar, utiliza comprensiones.
# Ejemplo de interpretación
# Si para 'ProductoA' y 'ProductoC' se obtiene {'ClienteA', 'ClienteB'}, significa que esos clientes
# aparecen como compradores de los dos productos.
def clientes_producto1_y_producto2(ventas, producto1, producto2):
    clientes_producto1 = {venta.cliente for venta in ventas if venta.producto == producto1}
    clientes_producto2 = {venta.cliente for venta in ventas if venta.producto == producto2}
    return clientes_producto1 & clientes_producto2

# Ejercicio 2
# Implementa diccionario_porcentaje_cantidad_producto(ventas). Debe devolver un diccionario
# que relacione cada producto con el porcentaje de unidades vendidas de ese producto respecto
# al total de unidades vendidas. Utiliza al menos una función auxiliar.
# Ejemplo de interpretación
# Si 'ProductoC' tiene asociado 3.56, sus unidades representan el 3,56 % del total de unidades
# vendidas
def auxiliar (ventas):
    total = {}
    for venta in ventas:
        clave = venta.producto
        if clave in total:
            total[clave] += venta.cantidad
        else:
            total[clave] = venta.cantidad
    return total

def diccionario_porcentaje_cantidad_producto(ventas):
    porcentaje_por_producto = {}
    total_cantidad = sum(venta.cantidad for venta in ventas)
    total = auxiliar(ventas)

    for clave in total:
        porcentaje_por_producto[clave] = total[clave] / total_cantidad * 100.0
    return porcentaje_por_producto

# Ejercicio 3
# Implementa producto_mas_vendido(ventas, clientes, n=3). Recibe una lista de ventas, un
# conjunto de nombres de clientes y un entero n. Debe devolver el nombre del producto más
# frecuente entre las n compras con mayor número de unidades realizadas por cualquiera de esos
# clientes.
# Ejemplo de interpretación
# Si entre las 5 compras de mayor cantidad de ClienteA y ClienteF el producto que más se repite
# es ProductoC, la función debe devolver 'ProductoC'.
def producto_mas_vendido(ventas, clientes, n=3):
    ventas_filtradas = [venta for venta in ventas if venta.cliente in clientes]
    ventas_ordenadas = sorted(ventas_filtradas, key=lambda venta: venta.cantidad, reverse=True)
    top_n_ventas = ventas_ordenadas[:n]
    productos = [venta.producto for venta in top_n_ventas]
    producto_mas_frecuente = max(set(productos), key=productos.count)
    return producto_mas_frecuente
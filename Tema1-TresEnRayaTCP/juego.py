"""Lógica del Tres en raya y protocolo de mensajes TCP.

Dos jugadores conectados por TCP comparten el mismo estado lógico de un tablero
de 3x3. El servidor juega con 'X' y comienza la partida; el cliente juega con 'O'.
No se utilizan hilos, clases propias ni librerías externas.
"""

TAMANO = 3
CASILLA_VACIA = " "


def crear_tablero():
    """Devuelve una matriz de 3x3 inicializada con casillas vacías."""
    return [[CASILLA_VACIA for _ in range(TAMANO)] for _ in range(TAMANO)]


def mostrar_tablero(tablero):
    """Muestra el tablero en consola con filas y columnas numeradas del 1 al 3."""
    print("\n    1   2   3")
    for indice_fila, fila in enumerate(tablero, start=1):
        print(f" {indice_fila}  " + " | ".join(fila))
        if indice_fila < TAMANO:
            print("   ---+---+---")
    print()


def jugada_valida(tablero, fila, columna):
    """Comprueba si (fila, columna) está entre 1 y 3 y la casilla está libre."""
    dentro_de_limites = 1 <= fila <= TAMANO and 1 <= columna <= TAMANO
    if not dentro_de_limites:
        return False

    return tablero[fila - 1][columna - 1] == CASILLA_VACIA


def colocar_ficha(tablero, fila, columna, simbolo):
    """Coloca 'X' u 'O' en la casilla indicada (coordenadas 1-3)."""
    if simbolo not in ("X", "O"):
        raise ValueError(f"Símbolo no válido: {simbolo}")
    if not jugada_valida(tablero, fila, columna):
        raise ValueError(f"Jugada no válida en ({fila}, {columna})")

    tablero[fila - 1][columna - 1] = simbolo


def comprobar_ganador(tablero):
    """Devuelve 'X' u 'O' si hay tres en raya; en caso contrario devuelve None."""
    # Comprobar filas (victoria horizontal)
    for fila in tablero:
        if fila[0] != CASILLA_VACIA and fila[0] == fila[1] == fila[2]:
            return fila[0]

    # Comprobar columnas (victoria vertical)
    for col in range(TAMANO):
        if (tablero[0][col] != CASILLA_VACIA
                and tablero[0][col] == tablero[1][col] == tablero[2][col]):
            return tablero[0][col]

    # Comprobar diagonal principal (arriba-izquierda a abajo-derecha)
    if (tablero[0][0] != CASILLA_VACIA
            and tablero[0][0] == tablero[1][1] == tablero[2][2]):
        return tablero[0][0]

    # Comprobar diagonal secundaria (arriba-derecha a abajo-izquierda)
    if (tablero[0][2] != CASILLA_VACIA
            and tablero[0][2] == tablero[1][1] == tablero[2][0]):
        return tablero[0][2]

    return None


def tablero_lleno(tablero):
    """Devuelve True si todas las casillas están ocupadas (útil para detectar empate)."""
    for fila in tablero:
        for casilla in fila:
            if casilla == CASILLA_VACIA:
                return False
    return True


def pedir_jugada(tablero):
    """Solicita al jugador una fila y columna válidas (1-3) sin perder el turno si falla."""
    while True:
        entrada = input("Elige fila y columna (1-3, ej. 2 1): ").strip()
        # Permitimos separar por espacio o por coma (ej. "2 1" o "2,1")
        entrada_normalizada = entrada.replace(",", " ")
        partes = entrada_normalizada.split()

        if len(partes) != 2:
            print("Formato no válido. Escribe dos números entre 1 y 3 (ej. 1 3).")
            continue

        try:
            fila = int(partes[0])
            columna = int(partes[1])
        except ValueError:
            print("Debes introducir números enteros entre 1 y 3.")
            continue

        if not (1 <= fila <= TAMANO and 1 <= columna <= TAMANO):
            print("Coordenadas fuera de rango. Fila y columna deben estar entre 1 y 3.")
            continue

        if not jugada_valida(tablero, fila, columna):
            print("Esa casilla ya está ocupada. Elige otra.")
            continue

        return fila, columna


def enviar_mensaje(conexion, mensaje):
    """Envía un mensaje de texto por TCP terminado en salto de línea ('\\n')."""
    datos = (mensaje + "\n").encode("utf-8")
    conexion.sendall(datos)


def recibir_mensaje(conexion):
    """Lee bytes del socket hasta encontrar '\\n'.

    TCP funciona como un flujo continuo de bytes, no por paquetes individuales:
    una llamada a recv(1024) podría leer medio mensaje o dos mensajes juntos.
    Leer de 1 en 1 hasta '\\n' garantiza recuperar exactamente un mensaje completo.
    """
    datos = bytearray()

    while True:
        fragmento = conexion.recv(1)
        if not fragmento:
            raise ConnectionError("El otro jugador se ha desconectado.")
        if fragmento == b"\n":
            break

        datos.extend(fragmento)
        if len(datos) > 64:
            raise ValueError("Mensaje recibido demasiado largo.")

    return datos.decode("utf-8")


def analizar_mensaje_jugada(mensaje):
    """Valida el protocolo 'JUGADA|fila|columna' y devuelve (fila, columna) como enteros."""
    partes = mensaje.split("|")
    if len(partes) != 3 or partes[0] != "JUGADA":
        raise ValueError(f"Mensaje inesperado del rival: {mensaje}")

    try:
        fila = int(partes[1])
        columna = int(partes[2])
    except ValueError as error:
        raise ValueError(f"Coordenadas inválidas en mensaje: {mensaje}") from error

    return fila, columna


def jugar(conexion, empieza):
    """Bucle principal de la partida compartido entre servidor y cliente.

    Parámetros:
        conexion: socket TCP ya conectado con el rival.
        empieza: True para el servidor (juega con 'X'), False para el cliente ('O').
    """
    tablero = crear_tablero()
    mi_ficha = "X" if empieza else "O"
    ficha_rival = "O" if empieza else "X"
    mi_turno = empieza
    partida_terminada = False

    print("\n¡Partida de Tres en raya iniciada!")
    print(f"Tu ficha es '{mi_ficha}'. El rival juega con '{ficha_rival}'.")
    mostrar_tablero(tablero)

    while not partida_terminada:
        if mi_turno:
            print(f"--- TU TURNO ({mi_ficha}) ---")
            fila, columna = pedir_jugada(tablero)

            # Actualizamos nuestro tablero y enviamos la jugada al rival
            colocar_ficha(tablero, fila, columna, mi_ficha)
            enviar_mensaje(conexion, f"JUGADA|{fila}|{columna}")
            mostrar_tablero(tablero)

            # Comprobamos si nuestra jugada termina la partida antes de ceder el turno
            if comprobar_ganador(tablero) == mi_ficha:
                print("¡HAS GANADO! Has completado tres en raya.")
                partida_terminada = True
            elif tablero_lleno(tablero):
                print("EMPATE. El tablero está lleno y nadie ha ganado.")
                partida_terminada = True
            else:
                mi_turno = False

        else:
            print(f"--- TURNO DEL RIVAL ({ficha_rival}) ---")
            print("Esperando jugada del rival...")

            mensaje = recibir_mensaje(conexion)
            fila, columna = analizar_mensaje_jugada(mensaje)

            # Validamos y aplicamos la jugada recibida en nuestra copia del tablero
            colocar_ficha(tablero, fila, columna, ficha_rival)
            print(f"El rival ha colocado '{ficha_rival}' en fila {fila}, columna {columna}.")
            mostrar_tablero(tablero)

            # Comprobamos si la jugada del rival termina la partida para salir sin quedar en recv()
            if comprobar_ganador(tablero) == ficha_rival:
                print("HAS PERDIDO. El rival ha completado tres en raya.")
                partida_terminada = True
            elif tablero_lleno(tablero):
                print("EMPATE. El tablero está lleno y nadie ha ganado.")
                partida_terminada = True
            else:
                mi_turno = True

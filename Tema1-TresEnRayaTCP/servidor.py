"""Jugador 1: servidor TCP para Tres en raya (ficha 'X'). Ejecutar primero."""

import socket
from juego import jugar

HOST = "0.0.0.0"  # Escucha en todas las interfaces de red IPv4 disponibles
PUERTO = 50505


def main():
    """Crea el socket servidor, espera un cliente y arranca la partida."""
    try:
        # AF_INET = IPv4, SOCK_STREAM = protocolo TCP fiable y orientado a conexión
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            # Permite reutilizar el puerto rápidamente si se reinicia el servidor
            servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            servidor.bind((HOST, PUERTO))
            servidor.listen(1)
            print(f"Jugador 1 (X). Esperando rival en el puerto {PUERTO}...")

            # accept() bloquea el programa hasta que se conecta el cliente
            conexion, direccion = servidor.accept()
            with conexion:
                print(f"Jugador 2 (O) conectado desde {direccion[0]}")
                jugar(conexion, empieza=True)

    except (OSError, ConnectionError, ValueError) as error:
        print(f"Error de conexión o de partida: {error}")
    except (KeyboardInterrupt, EOFError):
        print("\nPartida interrumpida.")


if __name__ == "__main__":
    main()

"""Jugador 2: cliente TCP para Tres en raya (ficha 'O'). Ejecutar tras el servidor."""

import socket
from juego import jugar

HOST = "127.0.0.1"  # IP local (cambiar por la IPv4 del servidor si está en otro PC)
PUERTO = 50505


def main():
    """Conecta con el servidor TCP y comienza la partida esperando el primer turno."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            cliente.connect((HOST, PUERTO))
            print(f"Jugador 2 (O). Conectado a {HOST}:{PUERTO}")
            jugar(cliente, empieza=False)

    except (OSError, ConnectionError, ValueError) as error:
        print(f"Error de conexión o de partida: {error}")
    except (KeyboardInterrupt, EOFError):
        print("\nPartida interrumpida.")


if __name__ == "__main__":
    main()

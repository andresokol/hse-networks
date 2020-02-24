import socket
import random


def get_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


PORT_RANGE = list(range(9000, 11000))


def get_random_port():
    return random.choice(PORT_RANGE)

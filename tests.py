import os
import socket

HOST: str = os.getenv('HW1_HOST', 'localhost')
PORT: int = int(os.getenv('HW1_PORT', '8080'))
QUIET: bool = True if os.getenv('HW1_QUIET', '') == '1' else False

BYTES_TO_LISTEN = 2 ** 15


def test_wrapper(test):
    def _wrapper() -> bool:
        if not QUIET:
            print(f'running {test.__name__}')
        try:
            with socket.create_connection((HOST, 21)) as connection:
                test(connection)
        except Exception as exc:
            if not QUIET:
                print(exc)
            return False
        return True

    return _wrapper


@test_wrapper
def _test_min(conn: socket.socket):
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode().split()[0] == '220'

    conn.send(b'SYST\r\n')
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode().split()[0] == '215'

    conn.send(b'QUIT\r\n')


@test_wrapper
def _test_set_mode(conn: socket.socket):
    conn.recv(BYTES_TO_LISTEN)

    conn.send(b'MODE S\r\n')
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode().split()[0] == '200'

    conn.send(b'STRU F\r\n')
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode().split()[0] == '200'

    conn.send(b'QUIT\r\n')


@test_wrapper
def _test_noop(conn: socket.socket):
    conn.recv(BYTES_TO_LISTEN)

    conn.send(b'NOOP\r\n')
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode().split()[0] == '200'


MINIMAL_TESTS = [_test_min, _test_set_mode, _test_noop]


def run_tests():
    for test in MINIMAL_TESTS:
        if not test():
            print('fail')
            return

    print('ok')

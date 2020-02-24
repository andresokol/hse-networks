import os
import socket

import utils

HOST: str = os.getenv('HW1_HOST', 'localhost')
PORT: int = int(os.getenv('HW1_PORT', '8080'))
QUIET: bool = True if os.getenv('HW1_QUIET', '') == '1' else False

BYTES_TO_LISTEN = 2 ** 15

with open(f'{os.path.dirname(os.path.abspath(__file__))}/static/demo.txt', 'rb') as f:
    FILE_TXT = f.read()
with open(f'{os.path.dirname(os.path.abspath(__file__))}/static/orange_pixel.png', 'rb') as f:
    FILE_PNG = f.read()


def test_wrapper(test):
    def _wrapper() -> bool:
        if not QUIET:
            print(f'running {test.__name__}')
        try:
            with socket.create_connection((HOST, PORT)) as connection:
                test(connection)
        except Exception as exc:
            if not QUIET:
                print(exc.with_traceback(exc.__traceback__))
            return False
        return True

    return _wrapper


def _dummy_start(conn: socket.socket):
    # welcome
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode().split()[0] == '220'

    conn.send(b'USER anonymous\r\n')
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode()[0] == '2'


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
    _dummy_start(conn)

    conn.send(b'MODE S\r\n')
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode().split()[0] == '200'

    conn.send(b'STRU F\r\n')
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode().split()[0] == '200'

    conn.send(b'QUIT\r\n')


@test_wrapper
def _test_noop(conn: socket.socket):
    _dummy_start(conn)

    conn.send(b'NOOP\r\n')
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode().split()[0] == '200'
    conn.send(b'NoOP\r\n')
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode().split()[0] == '200'
    conn.send(b'NOoP\r\n')
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode().split()[0] == '200'
    conn.send(b'noop\r\n')
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode().split()[0] == '200'


@test_wrapper
def _test_minimal_stor(conn: socket.socket):
    _dummy_start(conn)

    myport = utils.get_random_port()
    passive_socket = socket.socket()
    passive_socket.bind(('', myport))
    passive_socket.listen(1)

    port_representation = f'{utils.get_ip().replace(".", ",")},{myport // 256},{myport % 256}'
    conn.send(b'PORT ' + port_representation.encode() + b'\r\n')
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode()[0] == '2'

    conn.send(b'STOR demo.txt\r\n')
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode()[:3] == '150'
    conn_p, _ = passive_socket.accept()
    conn_p.send(FILE_TXT)
    conn_p.close()
    passive_socket.close()

    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode().split()[0][0] == '2'


@test_wrapper
def _test_minimal_retr(conn: socket.socket):
    _dummy_start(conn)

    myport = utils.get_random_port()
    passive_socket = socket.socket()
    passive_socket.bind(('', myport))
    passive_socket.listen(1)

    port_representation = f'{utils.get_ip().replace(".", ",")},{myport // 256},{myport % 256}'
    conn.send(b'PORT ' + port_representation.encode() + b'\r\n')
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode()[0] == '2'

    conn.send(b'RETR demo.txt\r\n')
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode()[:3] == '150'
    conn_p, _ = passive_socket.accept()
    received = conn_p.recv(BYTES_TO_LISTEN)
    conn_p.close()
    passive_socket.close()

    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode().split()[0][0] == '2'

    assert received.decode().strip() == FILE_TXT.decode().strip()

    conn.send(b'RETR whatever_final_fix_mock_2121.psd\r\n')
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode()[0] not in ['1', '2']


@test_wrapper
def _test_dir(conn: socket.socket):
    _dummy_start(conn)

    conn.send(b'PWD\r\n')
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode().strip()[0] == '2'

    conn.send(b'MKD andresokol_test_dir\r\n')
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode().strip()[0] == '2'

    conn.send(b'CWD andresokol_test_dir\r\n')
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode().strip()[0] == '2'

    conn.send(b'CDUP\r\n')
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode().strip()[0] == '2'

    conn.send(b'RMD andresokol_test_dir\r\n')
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode().strip()[0] == '2'

    conn.send(b'CWD andresokol_test_dir\r\n')
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode().strip()[0] != '2'


@test_wrapper
def _test_dele(conn: socket.socket):
    _dummy_start(conn)

    myport = utils.get_random_port()
    passive_socket = socket.socket()
    passive_socket.bind(('', myport))
    passive_socket.listen(1)

    port_representation = f'{utils.get_ip().replace(".", ",")},{myport // 256},{myport % 256}'
    conn.send(b'PORT ' + port_representation.encode() + b'\r\n')
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode()[0] == '2'

    conn.send(b'STOR demo2.txt\r\n')
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode()[:3] == '150'
    conn_p, _ = passive_socket.accept()
    conn_p.send(FILE_TXT)
    conn_p.close()
    passive_socket.close()
    conn.recv(BYTES_TO_LISTEN)

    conn.send(b'DELE demo2.txt\r\n')
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode()[0] == '2'

    conn.send(b'RETR demo2.txt\r\n')
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode()[0] not in ['1', '2']


@test_wrapper
def _test_pasv(conn: socket.socket):
    _dummy_start(conn)

    conn.send(b'PASV\r\n')
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode()[0] == '2'

    conn_str = data.decode().split()[1]
    limbs = conn_str.split(',')
    passive_addr = (f'{limbs[0]}.{limbs[1]}.{limbs[2]}.{limbs[3]}',
                    int(limbs[4]) * 256 + int(limbs[5]))
    print(passive_addr)

    conn.send(b'STOR pixel.png\r\n')
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode()[:3] == '150'

    with socket.create_connection(passive_addr) as conn:
        conn.send(FILE_PNG)
    data = conn.recv(BYTES_TO_LISTEN)
    assert data.decode()[0] == '2'


MINIMAL_TESTS = [_test_min, _test_set_mode, _test_noop, _test_minimal_stor, _test_minimal_retr]
DIR_TESTS = [_test_dir, _test_dele]
PASSIVE_TESTS = [_test_pasv]


def run_tests():
    TEST_MODE = os.getenv('HW1_TEST')
    if TEST_MODE == 'minimal' or not TEST_MODE:
        for test in MINIMAL_TESTS:
            if not test():
                print('fail')
                return

    if TEST_MODE == 'dir' or not TEST_MODE:
        for test in DIR_TESTS:
            if not test():
                print('fail')
                return

    if TEST_MODE == 'passive' or not TEST_MODE:
        for test in PASSIVE_TESTS:
            if not test():
                print('fail')
                return

    print('ok')

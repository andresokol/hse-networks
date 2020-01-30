import os
import socket
import threading
import typing as tp
import subprocess

PORT = 8083


class E(BaseException):
    def __init__(self, *args):
        super().__init__(*args)


def gen_new_port() -> tp.Tuple[int, str]:
    np = 9090
    return np, f'127,0,0,1,{np // 256},{np % 256}'


class Session:
    socket_: socket.socket
    connection: tp.Optional[socket.socket] = None
    port: int

    active_addr: tp.Optional[tp.Tuple[str, int]] = None
    current_dir: str = '/'

    def __init__(self, port):
        self.socket_ = socket.socket()
        self.socket_.bind(('', port))
        self.socket_.listen(1)
        self.port = port

        self.HANDLERS = {
            # system
            'USER': self._handle_user,
            'PASS': self._handle_pass,
            'SYST': self._handle_syst,
            'FEAT': self._handle_feat,

            # settings
            'TYPE': self._handle_type,
            'PASV': self._handle_pasv,
            'PORT': self._handle_port,

            'PWD': self._handle_pwd,
            'LIST': self._handle_list,
            'CWD': self._handle_cwd,
        }

        print(f'Server started at port {self.port}')

    def _send(self, msg: bytes):
        print(f'[{self.port}] SEND: {msg}')
        self.connection.send(msg + b'\r\n')

    def _send_active(self, lines: tp.List[bytes]):
        if not self.active_addr:
            print('dafuq')
            return

        with socket.create_connection(self.active_addr) as connection:
            for line in lines:
                print(f'[{self.active_addr}] SEND ACTIVE: {line}')
                connection.send(line + b'\r\n')

    def _handle_welcome(self):
        self._send(b'220 Service ready')

    def _handle_user(self, args: tp.Tuple[str]):
        self._send(b'331 User name ok, need password')

    def _handle_pass(self, args: tp.Tuple[str]):
        self._send(b'230 User logged in')

    def _handle_syst(self, args: tp.Tuple[str]):
        self._send(b'215 UNIX Type: L8')

    def _handle_feat(self, args: tp.Tuple[str]):
        self._send(b'211 No features')

    def _handle_type(self, args: tp.Tuple[str]):
        self._send(b'200 Set')

    def _handle_port(self, args: tp.Tuple[str]):
        parts = args[0].split(',')
        new_addr = '.'.join(parts[:4])
        new_port = int(parts[-2]) * 256 + int(parts[-1])
        self.active_addr = (new_addr, new_port)

        print(f'[{self.port}] Parsed address: {self.active_addr}')

        self._send(b'220 ok')

    def _handle_pasv(self, args: tp.Tuple[str]):
        new_port, port_msg = gen_new_port()
        self._send(b'215 ' + port_msg.encode())
        # t = threading.Thread(target=run, args=[new_port])
        # t.start()
        # print(f"[{self.port}] Started child server")
        # s = Session(new_port)
        # s.run()

    # # # # # # # # #
    # File commands #
    # # # # # # # # #

    def _handle_pwd(self, args: tp.Tuple[str]):
        self._send(b'257 "' + self.current_dir.encode() + b'" is the current directory')

    def _handle_list(self, args: tp.Tuple[str]):
        x = subprocess.run(args=('ls', '-l'), capture_output=True)

        self._send(b'150 Here comes the directory listing.')
        self._send_active(x.stdout.strip().split(b'\n'))
        self._send(b'226 Directory send OK.')

    def _handle_cwd(self, args: tp.Tuple[str]):
        self.current_dir = os.path.join(self.current_dir, args[0])
        print(f'[{PORT}] Set working dir to {self.current_dir}')
        self._send(b'250 Directory successfully changed.')

    def _fetch_command(self) -> tp.Tuple[str, tp.List[str]]:
        data = self.connection.recv(2048)
        if not data:
            raise E()

        print(f'[{self.port}] Received {len(data)} bytes: {data}')
        string = data.decode()
        args = string.strip().split(' ')
        return args[0], args[1:]

    def run(self):
        print(f'[{self.port}] Waiting for connection...')
        self.connection, addr = self.socket_.accept()
        print(f'[{self.port}] Connection accepted from {addr}')

        self._handle_welcome()

        while True:
            try:
                print(f'[{self.port}] Fetching command...')
                cmd, args = self._fetch_command()
                print(f'[{self.port}]', cmd, args)

                handler = self.HANDLERS.get(cmd.upper())
                if handler:
                    handler(args=args)
                else:
                    self._send(b'502 Not implemented')

            except E:
                return

    def __del__(self):
        if self.connection:
            self.connection.close()
        self.socket_.close()


def run(port):
    s = Session(port)
    while True:
        try:
            s.run()
        except Exception as e:
            s.socket_.close()
            raise e


if __name__ == '__main__':
    run(PORT)

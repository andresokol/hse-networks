import os
import socket
import typing as tp
import subprocess

HOST: str = os.getenv('HW1_HOST', 'localhost')
PORT: int = int(os.getenv('HW1_PORT', '8080'))
QUIET: bool = True if os.getenv('HW1_QUIET', '') == '1' else False
ROOT_DIR: str = os.getenv('HW1_DIRECTORY')
USER_FILE: str = os.getenv('HW1_USERS')
AUTH_DISABLED: bool = True if os.getenv('HW1_AUTH_DISABLED') == '1' else False


class E(BaseException):
    def __init__(self, *args):
        super().__init__(*args)


def gen_new_port() -> tp.Tuple[int, str]:
    np = 9090
    return np, f'127,0,0,1,{np // 256},{np % 256}'


def join_path(*args) -> str:
    resp: str = '/'.join(args)
    resp = resp.replace('//', '/')
    if resp[-1] == '/':
        resp = resp[:-1]
    return resp


class Mode:
    Stream = 'S'
    Block = 'B'
    Compressed = 'C'


class FileStructure:
    File = 'F'
    Record = 'R'
    Page = 'P'


class Session:
    socket_: socket.socket
    connection: tp.Optional[socket.socket] = None
    port: int

    active_addr: tp.Optional[tp.Tuple[str, int]] = None
    current_dir: str = '.'

    username: tp.Optional[str] = None
    is_authorized: bool = False

    mode = Mode.Stream
    file_structure = FileStructure.File

    def __init__(self):
        self.socket_ = socket.socket()
        self.socket_.bind(('', PORT))
        self.socket_.listen(1)
        self.port = PORT

        self.HANDLERS = {
            # login
            'USER': self._handle_user,
            'PASS': self._handle_pass,
            # 'CDUP': ,
            # 'SMNT': ,

            # system
            'SYST': self._handle_syst,
            'FEAT': self._handle_feat,
            'QUIT': self._handle_quit,

            # minimal
            'MODE': self._handle_mode,
            'STRU': self._handle_stru,
            'RETR': self._handle_retr,
            'STOR': self._handle_stor,
            'NOOP': self._handle_noop,

            # dir
            'CDUP': self._handle_cdup,
            'CWD': self._handle_cwd,
            'APPE': lambda x: x,
            'DELE': lambda x: x,
            'RMD': lambda x: x,
            'MKD': lambda x: x,
            'NLST': lambda x: x,

            # settings
            'TYPE': self._handle_type,
            'PASV': self._handle_pasv,
            'PORT': self._handle_port,

            'PWD': self._handle_pwd,
            'LIST': self._handle_list,
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

    def _fetch_active(self):
        if not self.active_addr:
            print('dafuq')
            return

        data = bytes()
        with socket.create_connection(self.active_addr) as connection:
            while True:
                data_block = connection.recv(4096)
                if not data_block:
                    break
                data += data_block
                print('.', end='')
        print('\nreceived', len(data), ' bytes')
        return data

    def _handle_welcome(self):
        self._send(b'220 Service ready')

    ####
    # login
    ###

    def _handle_user(self, args: tp.Tuple[str]):
        """
        230 User logged in, proceed.
        331 User name okay, need password.
        332 Need account for login.
        421 Service not available, closing control connection.
        500 Syntax error, command unrecognized.
        501 Syntax error in parameters or arguments.
        530 Not logged in.
        """
        self._send(b'331 User name ok, need password')

    def _handle_pass(self, args: tp.Tuple[str]):
        """
        202 Command not implemented, superfluous at this site.
        230 User logged in, proceed.
        331 User name okay, need password.
        332 Need account for login.
        421 Service not available, closing control connection.
        500 Syntax error, command unrecognized.
        501 Syntax error in parameters or arguments.
        503 Bad sequence of commands.
        530 Not logged in.
        """
        self._send(b'230 User logged in')

    def _handle_acct(self, args: tp.Tuple[str]):
        """
        230
        202
        530
        500, 501, 503, 421
        """
        pass
        # self._send(b'230 User logged in')

    def _handle_syst(self, args: tp.Tuple[str]):
        self._send(b'215 UNIX Type: L8')

    def _handle_feat(self, args: tp.Tuple[str]):
        self._send(b'211 No features')

    def _handle_type(self, args: tp.Tuple[str]):
        self._send(b'200 Set')

    def _handle_quit(self, args: tp.Tuple[str]):
        self._send(b'221 Bye!')

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
        self._send(
            f'257 "{os.path.normpath("/" + self.current_dir)}" is the current directory'.encode())

    def _handle_list(self, args: tp.Tuple[str]):
        cwd = os.path.normpath(ROOT_DIR + '/' + self.current_dir)
        print(f'listing ls -l {cwd}')
        x = ('ls', '-l', cwd)
        print(x)
        x = subprocess.run(args=x, capture_output=True)

        self._send(b'150 Here comes the directory listing.')
        self._send_active(x.stdout.strip().split(b'\n'))
        self._send(b'226 Directory send OK.')

    def _handle_mode(self, args: tp.Tuple[str]):
        """
        S - Stream
        B - Block
        C - Compressed

        200
        500, 501, 504, 421, 530
        """
        assert len(args) == 1
        assert args[0] in [Mode.Stream, Mode.Block, Mode.Compressed]
        self.mode = args[0]
        self._send(b'200 Command OK.')

    def _handle_stru(self, args: tp.Tuple[str]):
        # IS IT OKEY HERE?
        assert len(args) == 1
        assert args[0] in [Mode.Stream, Mode.Block, Mode.Compressed]
        self.mode = args[0]
        self._send(b'200 Command OK.')

    def _handle_retr(self, args: tp.Tuple[str]):
        """
        125, 150
        (110)
        226, 250
        425, 426, 451
        450, 550
        500, 501, 421, 530
        """
        # fix error codes
        assert len(args) == 1
        filename = args[0]

        filepath = os.path.normpath(ROOT_DIR + '/' + self.current_dir + '/' + filename)

        if os.path.isfile(filepath):
            self._send(b'550 Failed to open file.')  # FIXME
            return

        with open(filepath, 'rb') as file:
            file_data = file.read()

        self._send(b'150 File status okay; about to open data connection')
        self._send_active([file_data])
        self._send(b'226 Closing data connection, file transfer successful')

    def _handle_stor(self, args: tp.List[str]):
        """
        125, 150
        (110)
        226, 250
        425, 426, 451, 551, 552
        532, 450, 452, 553
        500, 501, 421, 530
        """
        # FIXME: args count
        assert len(args) == 1
        filename = args[0]

        filepath = os.path.normpath(ROOT_DIR + '/' + self.current_dir + '/' + filename)
        if not os.path.isfile(filepath):
            self._send(b'550 Failed to open file.')  # FIXME
            return

        with open(filepath, 'wb') as file:
            self._send(b'150 File status okay; about to open data connection.')  # FIXME: check
            data = self._fetch_active()
            file.write(data)
            self._send(b'226 Closing data connection, file transfer successful')  # FIXME: check

    def _handle_noop(self, args: tp.List[str]):
        self._send(b'200 Command OK.')

    def _handle_cdup(self, args: tp.List[str]):
        assert len(args) == 0
        assert self.current_dir != '.'

        self.current_dir = os.path.normpath(self.current_dir + '/../')

        self._send(b'200 Command OK.')

    def _handle_cwd(self, args: tp.Tuple[str]):
        """
        250
        500, 501, 502, 421, 530, 550
        """
        assert len(args) == 1
        self.current_dir = os.path.normpath(self.current_dir + '/' + args[0])

        print(f'[{PORT}] Setting working dir to {self.current_dir}')
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


def run():
    s = Session()
    while True:
        try:
            s.run()
        except Exception as e:
            s.socket_.close()
            raise e

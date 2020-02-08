import os
import server

if __name__ == '__main__':
    mode: str = os.getenv('HW1_MODE')
    if mode == 'server':
        print('running as server')
        server.run()
    elif mode == 'tests':
        print('tests')
    else:
        raise Exception(f'unknown mode {mode}')

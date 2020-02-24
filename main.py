import os
import server
import tests

if __name__ == '__main__':
    mode: str = os.getenv('HW1_MODE')
    if mode == 'server':
        server.run()
    elif mode == 'tests':
        tests.run_tests()
    else:
        raise Exception(f'unknown mode {mode}')

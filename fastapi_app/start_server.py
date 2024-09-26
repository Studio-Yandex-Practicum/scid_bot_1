import subprocess
import sys
import time


def run_migrations():
    try:
        print('Запуск миграций...')
        subprocess.run(['alembic', 'upgrade', 'head'], check=True)
    except subprocess.CalledProcessError as e:
        print(f'Ошибка применения миграций: {e}')
        sys.exit(1)


if __name__ == '__main__':
    time.sleep(10)
    run_migrations()
    print('Запуск сервера fastapi...')
    subprocess.run(
        [
            'uvicorn',
            'main:app',
            '--proxy-headers',
            '--host',
            '0.0.0.0',
            '--port',
            '8000',
        ]
    )

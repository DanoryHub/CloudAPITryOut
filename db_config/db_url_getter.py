import os

def get_postgres_url():
    DB_PW = os.environ.get('POSTGRES_PASSWORD')
    DB_USER = os.environ.get('POSTGRES_USER')
    DB_NAME = os.environ.get('POSTGRES_DB')
    DB_PORT = os.environ.get('POSTGRES_PORT')
    DB_HOST = os.environ.get('POSTGRES_HOST')

    return f'postgresql://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

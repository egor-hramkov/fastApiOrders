import os

DB_SETTINGS = {
    'USER': os.environ.get('db_user', 'postgres'),
    'PASSWORD': os.environ.get('db_password', 'python'),
    'HOST': os.environ.get('host', 'localhost'),
    'NAME': os.environ.get('db_name', 'sqlalchemy_fastapi'),
}

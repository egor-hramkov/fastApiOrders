import os

from dotenv import load_dotenv

load_dotenv()

DB_SETTINGS = {
    'USER': os.environ.get('db_user'),
    'PASSWORD': os.environ.get('db_password'),
    'HOST': os.environ.get('host'),
    'NAME': os.environ.get('db_name'),
}

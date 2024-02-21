import os

from dotenv import load_dotenv

load_dotenv()

DB_TEST_SETTINGS = {
    'USER': os.environ.get('test_db_user'),
    'PASSWORD': os.environ.get('test_db_password'),
    'HOST': os.environ.get('test_host'),
    'NAME': os.environ.get('test_db_name'),
}

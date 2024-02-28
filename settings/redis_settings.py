import os

from dotenv import load_dotenv

load_dotenv()

REDIS_SETTINGS = {
    'URL': os.getenv('REDIS_URL'),
    'PORT': os.getenv('REDIS_PORT'),
    'PASSWORD': os.getenv('REDIS_PASSWORD'),
}

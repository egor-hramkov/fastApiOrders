import os

from dotenv import load_dotenv

load_dotenv()

EMAIL_SETTINGS = {
    "MAIL_USERNAME": os.environ.get('MAIL_USERNAME'),
    "MAIL_PASSWORD": os.environ.get('MAIL_PASSWORD'),
    "MAIL_PORT": os.environ.get('MAIL_PORT', 587),
    "MAIL_SERVER": os.environ.get('MAIL_SERVER', "smtp.gmail.com"),
}

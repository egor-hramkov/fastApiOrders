from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from apps.user.models import User
from settings.db_settings import DB_SETTINGS

user = DB_SETTINGS['USER']
password = DB_SETTINGS['PASSWORD']
host = DB_SETTINGS['HOST']
db_name = DB_SETTINGS['NAME']
SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}/{db_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
metadata = User.metadata
session = Session(engine)

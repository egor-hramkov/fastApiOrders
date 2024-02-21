import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from tests.settings.db_settings import DB_TEST_SETTINGS

# Устанавливаем соединение с postgres
connection = psycopg2.connect(user=DB_TEST_SETTINGS['USER'], password=DB_TEST_SETTINGS['PASSWORD'])
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# Создаем курсор для выполнения операций с базой данных
db_name = DB_TEST_SETTINGS['NAME']
cursor = connection.cursor()
sql_create_database = f'create database {db_name}'
# Создаем базу данных
cursor.execute(sql_create_database)
# Закрываем соединение
cursor.close()
connection.close()

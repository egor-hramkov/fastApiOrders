# Локальное разворачивание проекта
* Python 3.11, PSQL
* pip install -r requirements.txt
* скопировать env.example в .env
* в .env ввести свои настройки подключения к БД
* применить миграции командой alembic upgrade head
* Запустить main.py

# Разворачивание в докере

* cd docker
* docker-compose up -d

# Полезные команды

* Создание миграций - alembic revision -m "название"


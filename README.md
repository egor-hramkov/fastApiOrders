# Локальное разворачивание проекта
* Python 3.11, PSQL
* pip install -r requirements.txt
* скопировать env.example в .env
* в .env ввести свои настройки подключения к БД
* применить миграции командой alembic upgrade head
* Запустить main.py

# Для создания тестовой БД, предварительно настроив .env
python tests/create_test_db.py

# Разворачивание в докере

* cd docker
* docker-compose up -d
* Проверить в контейнере app, что приложение стало прослушивать брокера кафки, иначе перезапустить контейнер app
* Кафка в докере работает на 9092 порту, если присылать сообщения из вне - кафка прослушивает localhost:9094

Бэк запускается на localhost:8000

Админка PGAdmin запускается на localhost:5050

Kafka-Ui запускается на localhost:8090

# Полезные команды

* Создание миграций - alembic revision -m "название" --autogenerate

# Используем базовый образ Python
FROM python:3.11-slim-buster

# Установка зависимостей
RUN pip install --no-cache-dir fastapi==0.103.1 loguru==0.7.0 uvicorn==0.23.2 \
uvloop==0.17.0 psycopg2-binary==2.9.9 python-dotenv==1.0.0 pydantic-settings==2.0.3

# Копирование файлов проекта в контейнер
COPY . .
WORKDIR .

EXPOSE 8000

# # Установка PostgreSQL клиента
# RUN apt-get update && apt-get install -y postgresql-client

# # Переменные окружения
# ENV POSTGRES_HOST=postgres
# ENV POSTGRES_PORT=5432
# ENV POSTGRES_DB=mydatabase
# ENV POSTGRES_USER=myuser
# ENV POSTGRES_PASSWORD=mypassword

# Запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--use-colors"]
# CMD ["python3", "./app/main.py"]
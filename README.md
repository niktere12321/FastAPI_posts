# Проект FastAPI_posts

## Описание

FastAPI_posts это сервис для публикации постов.

Пользователи могут создать пост, а так же оценивать посты других пользователей

## Технологии
- Python 3.9,13
- fastapi==0.78.0
- SQLAlchemy==2.0.17
- alembic==1.7.7

## Установка проекта локально

* Склонировать репозиторий на локальную машину:
```bash
git clone https://github.com/niktere12321/FastAPI_posts.git
```
```bash
cd FastAPI_posts
```

- Создать и заполнить по образцу .env-файл
```
APPLICATION_URL=<...>
POSTGRES_DB=<...>
POSTGRES_USER=<...>
POSTGRES_PASSWORD=<...>
DB_HOST=<...>
DB_PORT=<...>
SECRET=<...>
```

* Cоздать и активировать виртуальное окружение:

```bash
python -m venv venv
```

```bash
source venv/Scripts/activate
```

* Установить зависимости из файла requirements.txt:

```bash
python3 -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

* Выполните миграции:
```bash
alembic upgrade head
```

* Запустить сервис:
```bash
cd app/
```
```bash
python application.py
```

---
## Об авторе

Терехов Никита Алексеевич
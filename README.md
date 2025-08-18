

# ORM Flask SQL Library API

## Описание
Проект представляет собой RESTful API для управления библиотекой книг и авторов, реализованное с использованием Python, Flask и SQLAlchemy. API позволяет создавать, читать, обновлять и удалять (CRUD) книги и авторов, а также обеспечивает документацию с помощью Swagger.

## Архитектура проекта

```` markdown

ORM\_Flask\_SQL/
├── app.py                  # Основной файл приложения Flask
├── models/
│   ├── **init**.py         # Инициализация SQLAlchemy
│   ├── book\_model.py       # Модель Book
│   └── author\_model.py     # Модель Author
├── instance/
│   └── library.db          # SQLite база данных
├── README.md               # Документация проекта
└── requirements.txt        # Зависимости проекта

````

### Технологии
- Python 3.x
- Flask
- Flask-SQLAlchemy
- Swagger (Flasgger)
- SQLite

## Особенности
- Полный CRUD для книг и авторов.
- Использование ORM SQLAlchemy для работы с базой данных.
- Связь «один ко многим» между авторами и книгами.
- Swagger документация для всех эндпоинтов.
- Обработка ошибок с кастомными сообщениями (`400`, `404`, `500`).

## Эндпоинты API

### Книги
- **GET /books** — получить все книги.
- **POST /books** — добавить новую книгу.
- **GET /books/<book_id>** — получить книгу по ID.
- **PUT /books/<book_id>** — обновить книгу по ID.
- **DELETE /books/<book_id>** — удалить книгу по ID.

### Авторы
- **GET /authors** — получить всех авторов.
- **POST /authors** — добавить нового автора.
- **GET /authors/<author_id>** — получить автора по ID.
- **PUT /authors/<author_id>** — обновить автора по ID.
- **DELETE /authors/<author_id>** — удалить автора по ID (только если у него нет книг).

## Запуск проекта

1. Клонируйте репозиторий:
```bash
git clone <url_репозитория>
cd ORM_Flask_SQL
````

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Запустите приложение:

```bash
python app.py
```

4. Swagger документация доступна по адресу:

```
http://127.0.0.1:5000/apidocs/
```

## Примеры запросов

**Добавление автора:**

```bash
POST /authors
{
    "name": "Leo Tolstoy"
}
```

**Добавление книги:**

```bash
POST /books
{
    "title": "War and Peace",
    "author": "Leo Tolstoy"
}
```

## Цель проекта

Продемонстрировать навыки работы с Flask, SQLAlchemy, REST API, Swagger и умение строить полноценные backend-приложения с CRUD функционалом и базой данных.



# FastAPI Demo

## Приложение для ветеринарной клиники

### Автор: Дубровец Виталий Олегович

- Создан репозиторий
- Поднята база PostgreSQL на render.com
- Интегрированы переменные среды в приложение
- Реализован API в соответствии с документацией
- Создан шаблон файла с секретами (.env.example)
- Задеплоено приложение на render.com

Ccылка на приложение: https://fast-api-u9xh.onrender.com/

---

## Описание структуры проекта
- <code>crud.py</code>
  - CRUD-функции для работы с БД (ORM от sqlalchemy)
- <code>db.py</code>
  - Функции для подключения к БД Postgresql (psycopg2)
  - Используем переменные среды через python-dotenv
- <code>main.py</code>
  - Контроллеры FastAPI
- <code>models.py</code>
  - Модели данных (sqlalchemy)
- <code>schemas.py</code>
  - Схемы валидации данных (pydantic)
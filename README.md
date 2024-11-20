# Todo Application
## _Yet another todo application_

A full stack todo application written using FastAPI, Sqlite and Jinja with OAuth for authentication and authorization. 

[Try it out](https://todoapp-fastapi-bmrh.onrender.com)

## Udemy
 - [FastAPI course](https://www.udemy.com/course/fastapi-the-complete-course/)

## Tech
 - Python3
 - Poetry
 - FastAPI
 - Sqlalchemy
 - Jinja2
 - OAuth
 - Pytest
 - Alembic

## Running locally

```sh
cd fastapi-udemy-course
poetry install
poetry run proj03
```

Alternatively, you could also run

```sh
uvicorn fastapi_udemy_course.proj03_todo.app:app --host 0.0.0.0 --port 8000
```

## Testing
```sh
poetry run pytest .
```

## Links
- [FastAPI course](https://www.udemy.com/course/fastapi-the-complete-course/)
- [Render cloud service](https://dashboard.render.com/)

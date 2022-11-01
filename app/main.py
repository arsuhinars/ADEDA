from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .db import SessionLocal, engine
from .models import Base, User

# Генерируем таблицы для моделей
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
def index():
    return JSONResponse({'hello': 'world', 'pi': 3.34, 'happy': True})

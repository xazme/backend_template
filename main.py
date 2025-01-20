# app/main.py
from fastapi import FastAPI
from app.core.database.init_db import create_table
from app.core.database.engine import engine
from app.core.database.sessions import async_session

app = FastAPI(lifespan=lambda: lifespan_handler())


async def lifespan_handler():

    print("Инициализация базы данных...")
    await create_table()

    print("Закрытие сессий и завершение работы с базой данных...")
    await engine.dispose()

if __name__ == "__main__":

    import uvicorn
    uvicorn.run("main:app", reload=True)

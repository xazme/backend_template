import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import create_table


@asynccontextmanager
async def lifespan_handler(app):
    create_table()
    yield

app = FastAPI(lifespan=lifespan_handler)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

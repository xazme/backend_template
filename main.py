import uvicorn
from app.api.v1 import router as router_v1
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import create_table
from middleware import TestMiddleWare


@asynccontextmanager
async def lifespan_handler(app):
    # await create_table()
    yield


app = FastAPI(lifespan=lifespan_handler)
app.add_middleware(TestMiddleWare)
app.include_router(router=router_v1)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

import uvicorn
from contextlib import asynccontextmanager
from typing import Optional
from sqlmodel import Field
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from fastapi import FastAPI
from fastapi import HTTPException


engine = create_async_engine("sqlite+aiosqlite://", echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    counter: int = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int) -> Item:
    async with async_session() as session:
        item = await session.get(Item, item_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/items/{item_id}")
async def read_item(item_id: int) -> Item:
    async with async_session() as session:
        item = await session.get(Item, item_id)
        if item is None:
            item = Item(id=item_id, counter=1)
        else:
            item.counter += 1
        session.add(item)
        await session.commit()
    return item


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import Base, engine
from sqlalchemy import select, Result
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from app.core.models import *
from sqlalchemy.exc import MultipleResultsFound
from typing import Type, TypeVar

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

T = TypeVar("T", Worker, Task)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def check_model(session: AsyncSession, model: Type[T]):
    stmt = select(type(model)).where(type(model).id == model.id)
    result: Result = await session.execute(stmt)
    entity = result.scalar_one_or_none()
    return entity


async def create_worker(session: AsyncSession, name: str, email: str):
    check_worker_info = await check_model(
        session=session,
        model=Worker(name=name, email=email),
    )

    if check_worker_info:
        raise Exception("worker уже есть")

    new_worker = Worker(name=name, email=email)
    session.add(new_worker)
    await session.commit()
    return new_worker


async def create_task(session: AsyncSession, title: str, description: str):
    check_task_info = await check_model(
        session=session,
        model=Task(title=title, description=description),
    )

    if check_task_info:
        raise Exception("task уже есть")

    new_task = Task(title=title, description=description)
    session.add(new_task)
    await session.commit()
    return new_task


async def change_status_assoc(session: AsyncSession, task: Task):
    try:
        stmt = (
            select(TaskWorkerAssoc).where(TaskWorkerAssoc.task_id == task.id).limit(1)
        )
        result: Result = await session.execute(stmt)
        assoc = result.scalar_one_or_none()

        if assoc is None:
            raise Exception("ПОШЕЛ НАХУЙ")

        assoc.status = Status.complete.name
        await session.commit()

    except MultipleResultsFound:
        raise Exception("Найдено несколько ассоциаций с задачей")


async def get_all_tasks(session: AsyncSession):
    stmt = select(TaskWorkerAssoc)

    result: Result = await session.execute(stmt)
    tasks = result.scalars().all()

    z = [f"{task.status} and {task.task.title}" for task in tasks]
    return z


async def main():
    await create_tables()
    async with async_session() as session:
        # Создание воркеров
        try:
            worker1 = await create_worker(
                session, name="John Doe", email="johndoe@example.com"
            )
            print(f"Создан worker: {worker1.name}")

            worker2 = await create_worker(
                session, name="Jane Smith", email="janesmith@example.com"
            )
            print(f"Создан worker: {worker2.name}")

            worker3 = await create_worker(
                session, name="Alice Johnson", email="alicejohnson@example.com"
            )
            print(f"Создан worker: {worker3.name}")
        except Exception as e:
            print(f"Ошибка при создании воркера: {e}")

        # Создание тасков
        try:
            task1 = await create_task(
                session, title="Task 1", description="Description for task 1"
            )
            print(f"Создан task: {task1.title}")

            task2 = await create_task(
                session, title="Task 2", description="Description for task 2"
            )
            print(f"Создан task: {task2.title}")

            task3 = await create_task(
                session, title="Task 3", description="Description for task 3"
            )
            print(f"Создан task: {task3.title}")
        except Exception as e:
            print(f"Ошибка при создании таска: {e}")

        worker1 = await session.scalar(
            select(Worker)
            .where(Worker.id == worker1.id)
            .options(selectinload(Worker.task_info).selectinload(TaskWorkerAssoc.task))
        )
        worker2 = await session.scalar(
            select(Worker)
            .where(Worker.id == worker2.id)
            .options(selectinload(Worker.task_info).selectinload(TaskWorkerAssoc.task))
        )
        worker3 = await session.scalar(
            select(Worker)
            .where(Worker.id == worker3.id)
            .options(selectinload(Worker.task_info).selectinload(TaskWorkerAssoc.task))
        )

        worker1.task_info.append(TaskWorkerAssoc(task=task1))
        worker2.task_info.append(TaskWorkerAssoc(task=task2))
        worker3.task_info.append(TaskWorkerAssoc(task=task1))

        await session.commit()

        await change_status_assoc(session=session, task=task1)
        tasks = await get_all_tasks(session=session)

        print(tasks)


asyncio.run(main())

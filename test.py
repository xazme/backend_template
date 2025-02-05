import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import Base, engine
from sqlalchemy import select

from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from app.core.database import engine
from app.core.models import Book, Reader, BookReaderAssoc, Author

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def create_book(session: AsyncSession, title: str, author: Author):
    new_book = Book(title=title, author=author)
    session.add(new_book)
    await session.commit()
    return new_book


async def create_reader(session: AsyncSession, name: str, email: str):
    new_reader = Reader(name=name, email=email)
    session.add(new_reader)
    await session.commit()
    return new_reader


async def create_author(session: AsyncSession, name: str):
    new_author = Author(name=name)
    session.add(new_author)
    await session.commit()
    return new_author


async def reader_get_book(ses: AsyncSession, book: Book, reader: Reader):
    if not book.availible:
        raise Exception("книга недоступна")

    reader.book_info.append(BookReaderAssoc(book=book))

    book.availible = False
    await ses.commit()
    print(f"книга была взята {reader.name}")


async def reader_return_book(ses: AsyncSession, book: Book, reader: Reader):
    if book.availible:
        raise Exception("книга не бралась")

    reader.book_info.pop(BookReaderAssoc(book=book))

    book.availible = True
    await ses.commit()
    print(f"книга была возвращена {reader.name}")


async def get_reader_book(ses: AsyncSession, reader: Reader):
    stmt = (
        select(Reader)
        .where(Reader.id == reader.id)
        .options(selectinload(Reader.book_info).joinedload(BookReaderAssoc.book))
    )


async def main():
    await create_tables()
    async with async_session() as session:

        # authors
        author1 = await create_author(session, "OLEG")
        author2 = await create_author(session, "OLEG CLONE")
        author3 = await create_author(session, "OLEG CLONE CLONE")
        author4 = await create_author(session, "super oleg master 123")

        # books
        book1 = await create_book(session, "какашки", author1)
        book2 = await create_book(session, "алхимия это пизде", author2)
        book3 = await create_book(session, "ебаный рот", author3)
        book4 = await create_book(session, "какаю в туалети", author4)

        # readers
        reader1 = await create_reader(session, "PISYA", "shaboldaena@gmail.com")
        reader2 = await create_reader(session, "ebaniu", "shol123daena@gmail.com")
        reader3 = await create_reader(session, "zxcqwe", "12shazxcna@gmail.com")
        reader4 = await create_reader(session, "dedad", "colshpoaaena@gmail.com")

        # readers loading
        reader1 = await session.scalar(
            select(Reader)
            .where(Reader.id == reader1.id)
            .options(selectinload(Reader.book_info))
        )

        reader2 = await session.scalar(
            select(Reader)
            .where(Reader.id == reader2.id)
            .options(selectinload(Reader.book_info))
        )

        reader3 = await session.scalar(
            select(Reader)
            .where(Reader.id == reader3.id)
            .options(selectinload(Reader.book_info))
        )

        reader4 = await session.scalar(
            select(Reader)
            .where(Reader.id == reader4.id)
            .options(selectinload(Reader.book_info))
        )

        readers = [reader1, reader2, reader3, reader4]
        books = [book1, book2, book3, book4]

        await reader_get_book(session, book1, reader1)
        await reader_get_book(session, book4, reader1)
        await reader_get_book(session, book2, reader2)
        await reader_get_book(session, book3, reader3)
        # await reader_get_book(session, book4, reader4)

        # await reader_get_book(session, book1, reader3)

        reader = await get_reader_book(session, reader1)

        for elem in reader:
            print(elem.name, elem.email)
            for book in elem.book_info:
                print(book.book.title)


asyncio.run(main())

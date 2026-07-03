import asyncpg
import os
from collections.abc import AsyncGenerator
from datetime import date, time

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import selectinload

os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5434")
os.environ.setdefault("DB_USER", "danil")
os.environ.setdefault("DB_PASS", "postgres")
os.environ.setdefault("DB_NAME", "meeting_room_booking_test")
os.environ.setdefault("JWT_SECRET", "test-secret")

from app.config import settings
from app.database import Base, get_db
from app.main import app
from app.models.booking import Booking
from app.models.room import Room
from app.models.slot import Slot
from app.models.user import User, UserRole
from app.services.auth import hash_password

dsn = settings.database_url.replace("+asyncpg", "")


@pytest_asyncio.fixture(autouse=True)
async def clean_tables():
    conn = await asyncpg.connect(dsn)
    try:
        for table in ("bookings", "slots", "rooms", "users", "alembic_version"):
            await conn.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE")
    finally:
        await conn.close()


@pytest_asyncio.fixture
async def engine_and_session():
    engine = create_async_engine(settings.database_url, echo=False, pool_size=2)
    session_maker = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    yield engine, session_maker
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(engine_and_session) -> AsyncGenerator[AsyncSession, None]:
    _, session_maker = engine_and_session
    async with session_maker() as session:
        yield session


async def _override_get_db_factory(session_maker):
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        async with session_maker() as session:
            yield session

    return override_get_db


@pytest_asyncio.fixture
async def client(engine_and_session) -> AsyncGenerator[AsyncClient, None]:
    _, session_maker = engine_and_session
    overrides = app.dependency_overrides
    overrides[get_db] = await _override_get_db_factory(session_maker)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    overrides.clear()


@pytest_asyncio.fixture
async def admin_user(db_session: AsyncSession) -> User:
    user = User(
        login="admin",
        password_hash=hash_password("admin"),
        full_name="Admin",
        role=UserRole.admin,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def regular_user(db_session: AsyncSession) -> User:
    user = User(
        login="user",
        password_hash=hash_password("user"),
        full_name="User",
        role=UserRole.user,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def room_with_slots(db_session: AsyncSession) -> Room:
    room = Room(name="Test Room", capacity=10)
    db_session.add(room)
    await db_session.flush()
    slots = [
        Slot(room_id=room.id, start_time=time(9, 0), end_time=time(11, 0)),
        Slot(room_id=room.id, start_time=time(13, 0), end_time=time(15, 0)),
    ]
    db_session.add_all(slots)
    await db_session.commit()

    result = await db_session.execute(
        select(Room).where(Room.id == room.id).options(selectinload(Room.slots))
    )
    return result.scalar_one()


@pytest_asyncio.fixture
async def user_token(client: AsyncClient, regular_user: User) -> str:
    response = await client.post(
        "/api/v1/auth/login",
        json={"login": "user", "password": "user"},
    )
    return response.json()["access_token"]


@pytest_asyncio.fixture
async def admin_token(client: AsyncClient, admin_user: User) -> str:
    response = await client.post(
        "/api/v1/auth/login",
        json={"login": "admin", "password": "admin"},
    )
    return response.json()["access_token"]


@pytest_asyncio.fixture
async def booking(
    db_session: AsyncSession,
    regular_user: User,
    room_with_slots: Room,
) -> Booking:
    slot = room_with_slots.slots[0]
    booking = Booking(
        user_id=regular_user.id,
        room_id=room_with_slots.id,
        slot_id=slot.id,
        date=date(2026, 7, 10),
    )
    db_session.add(booking)
    await db_session.commit()
    await db_session.refresh(booking)
    return booking

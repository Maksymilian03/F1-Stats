import os
from unittest.mock import AsyncMock

import pytest
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from database import Base, get_db
from main import app

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql://placeholder:placeholder@localhost:5432/placeholder")
TEST_DATABASE_URL = TEST_DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

@pytest.fixture
def fake_drivers():
    return {
        44: {"driver_number": 44, "full_name": "Lewis Hamilton", "team_name": "Mercedes"},
        3: {"driver_number": 3, "full_name": "Max Verstappen", "team_name": "Red Bull"},
        16: {"driver_number": 16, "full_name": "Charles Leclerc", "team_name": "Ferrari"},
        6: {"driver_number": 6, "full_name": "Sergio Perez", "team_name": "Red Bull"},
        45: {"driver_number": 45, "full_name": "Carlos Sainz", "team_name": "Ferrari"},
        77: {"driver_number": 77, "full_name": "Valtteri Bottas", "team_name": "Mercedes"},
    }

@pytest.fixture
def fake_sprints_results():
    return [
  [{"position": 1, "driver_number": 3, "points": 8, "session_key": 9579},
    {"position": 2, "driver_number": 44, "points": 7, "session_key": 9579},
    {"position": 3, "driver_number": 16, "points": 6, "session_key": 9579},
    {"position": 4, "driver_number": 6, "points": 5, "session_key": 9579},
    {"position": 5, "driver_number": 45, "points": 4, "session_key": 9579},
    {"position": 6, "driver_number": 77, "points": 3, "session_key": 9579}],

  [{"position": 1, "driver_number": 44, "points": 8, "session_key": 9888},
    {"position": 2, "driver_number": 3, "points": 7, "session_key": 9888},
    {"position": 3, "driver_number": 16, "points": 6, "session_key": 9888},
    {"position": 4, "driver_number": 6, "points": 5, "session_key": 9888},
    {"position": 5, "driver_number": 45, "points": 4, "session_key": 9888},
    {"position": 6, "driver_number": 77, "points": 3, "session_key": 9888}],

  [{"position": 1, "driver_number": 16, "points": 8, "session_key": 9571},
    {"position": 2, "driver_number": 3, "points": 7, "session_key": 9571},
    {"position": 3, "driver_number": 44, "points": 6, "session_key": 9571},
    {"position": 4, "driver_number": 6, "points": 5, "session_key": 9571},
    {"position": 5, "driver_number": 45, "points": 4, "session_key": 9571},
    {"position": 6, "driver_number": 77, "points": 3, "session_key": 9571}]
  ]

@pytest.fixture
def fake_races_results():
    return [
    [{"position": 1, "driver_number": 3, "points": 25, "session_key": 9575},
        {"position": 2, "driver_number": 44, "points": 18, "session_key": 9575},
        {"position": 3, "driver_number": 16, "points": 15, "session_key": 9575},
        {"position": 4, "driver_number": 6, "points": 12, "session_key": 9575},
        {"position": 5, "driver_number": 45, "points": 10, "session_key": 9575},
        {"position": 6, "driver_number": 77, "points": 8, "session_key": 9575}],

    [{"position": 1, "driver_number": 44, "points": 25, "session_key": 9573},
        {"position": 2, "driver_number": 3, "points": 18, "session_key": 9573},
        {"position": 3, "driver_number": 16, "points": 15, "session_key": 9573},
        {"position": 4, "driver_number": 6, "points": 12, "session_key": 9573},
        {"position": 5, "driver_number": 45, "points": 10, "session_key": 9573},
        {"position": 6, "driver_number": 77, "points": 8, "session_key": 9573}],

    [{"position": 1, "driver_number": 3, "points": 25, "session_key": 9572},
        {"position": 2, "driver_number": 16, "points": 18, "session_key": 9572},
        {"position": 3, "driver_number": 44, "points": 15, "session_key": 9572},
        {"position": 4, "driver_number": 6, "points": 12, "session_key": 9572},
        {"position": 5, "driver_number": 45, "points": 10, "session_key": 9572},
        {"position": 6, "driver_number": 77, "points": 8, "session_key": 9572}]
    ]

@pytest.fixture
def fake_race_keys():
    return [9575, 9573, 9572]

@pytest.fixture
def fake_empty_race_keys():
    return []

@pytest.fixture
def fake_sprint_keys():
    return [9579, 9888, 9571]

@pytest.fixture
def fake_empty_sprint_keys():
    return []



@pytest.fixture
def fake_cached_data():
    return [
        {"driver_number": 3, "full_name": "Max Verstappen", "points": 100, "wins": 5},
        {"driver_number": 44, "full_name": "Lewis Hamilton", "points": 90, "wins": 4},
        {"driver_number": 16, "full_name": "Charles Leclerc", "points": 80, "wins": 3},
    ]


@pytest.fixture
def mock_session():
    return AsyncMock()


@pytest.fixture(scope='session')
async def test_engine():
    test_engine = create_async_engine(TEST_DATABASE_URL)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield test_engine
    await test_engine.dispose()


@pytest.fixture(scope='session')
def test_session_factory(test_engine):
    return async_sessionmaker(test_engine, expire_on_commit=False)

@pytest.fixture
async def db_session(test_session_factory):
    async with test_session_factory() as session:
        yield session
        table_names = ", ".join(Base.metadata.tables.keys())
        await session.execute(text(f"TRUNCATE TABLE {table_names} RESTART IDENTITY;"))
        await session.commit()


@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()




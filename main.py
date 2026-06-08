from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Path
from sqlalchemy.ext.asyncio import AsyncSession

from database import Base, engine, get_db
from schemas import ConstructorEntry, Driver, RaceResult, StandingsEntry
from services import (
    CURRENT_YEAR,
    fetch_drivers,
    get_constructor_standings,
    get_driver_standings,
    get_race_results,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "F1 Stats"}


@app.get('/drivers/', response_model=list[Driver])
async def drivers_endpoint():
    list_of_drivers = await fetch_drivers()
    return list(list_of_drivers.values())


@app.get('/results/{year}/{country}/', response_model=list[RaceResult])
async def race_results_endpoint(
    year: int = Path(..., ge=2023, le=CURRENT_YEAR),
    country: str = Path(...),
):
    return await get_race_results(year, country)


SessionDep = Annotated[AsyncSession, Depends(get_db)]

@app.get('/standings/constructors/{year}/', response_model=list[ConstructorEntry])
async def constructor_standings_endpoint(
    year: int = Path(
        ..., ge=2023, le=CURRENT_YEAR),
    session: SessionDep = None):
    return await get_constructor_standings(year, session)


@app.get('/standings/{year}/', response_model=list[StandingsEntry])
async def standings_endpoint(
    year: int = Path(
        ..., ge=2023, le=CURRENT_YEAR,
        description=f"Rok musi być pomiędzy 2023 a {CURRENT_YEAR}"
        ),
    session: SessionDep = None
    ):
    return await get_driver_standings(year, session)

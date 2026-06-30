from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Path
from sqlalchemy.ext.asyncio import AsyncSession

from database import Base, engine, get_db
from schemas import CompareResponse, ConstructorEntry, Driver, RaceResult, StandingsEntry
from services import (
    CURRENT_YEAR,
    fetch_drivers,
    get_comparison_drivers,
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


@app.get('/standings/constructors/{year}/', response_model=list[ConstructorEntry])
async def constructor_standings_endpoint(
    year: int = Path(
        ..., ge=2023, le=CURRENT_YEAR),
      session: AsyncSession = Depends(get_db)): # noqa B008
    return await get_constructor_standings(year, session)


@app.get('/standings/{year}/', response_model=list[StandingsEntry])
async def standings_endpoint(
    year: int = Path(
        ..., ge=2023, le=CURRENT_YEAR,
        description=f"Rok musi być pomiędzy 2023 a {CURRENT_YEAR}"
        ),
    session: AsyncSession = Depends(get_db) # noqa B008
    ):
    return await get_driver_standings(year, session)


@app.get('/compare/{year}/{driver1_number}/{driver2_number}/', response_model=CompareResponse)
async def compare_endpoint(
    year: int = Path(
        ..., ge=2023, le=CURRENT_YEAR,
        description=f"Rok musi być pomiędzy 2023 a {CURRENT_YEAR}"
        ),
    driver1_number: int = Path(
        ...,
        ge=1,
        le=99,
        description="Number of first driver must be 1-99"
    ),
    driver2_number: int = Path(
        ...,
        ge=1,
        le=99,
        description="Number of second driver must be 1-99"
    ),
    session: AsyncSession = Depends(get_db) # noqa B008
):
    return await get_comparison_drivers(year, driver1_number, driver2_number, session)

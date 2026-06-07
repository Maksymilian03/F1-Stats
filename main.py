
from fastapi import FastAPI, Path, Depends
from contextlib import asynccontextmanager

from schemas import ConstructorEntry, Driver, RaceResult, StandingsEntry
from services import (
    CURRENT_YEAR,
    fetch_drivers,
    get_constructor_standings,
    get_driver_standings,
    get_race_results,
)
from database import engine, Base, get_db
from sqlalchemy.ext.asyncio import AsyncSession

import models

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
async def constructor_standings_endpoint(year: int = Path(..., ge=2023, le=CURRENT_YEAR)):
    return await get_constructor_standings(year)


@app.get('/standings/{year}/', response_model=list[StandingsEntry])
async def standings_endpoint(
    year: int = Path(
        ..., ge=2023, le=CURRENT_YEAR,
        description=f"Rok musi być pomiędzy 2023 a {CURRENT_YEAR}"
        ),
    session: AsyncSession = Depends(get_db)
    ):
    return await get_driver_standings(year, session)





from fastapi import FastAPI, Path
from schemas import Driver, RaceResult, StandingsEntry

from services import fetch_drivers, get_standings, get_race_results




app = FastAPI()


@app.get("/")
def root():
    return {"message": "F1 Stats"}


@app.get('/drivers/', response_model=list[Driver])
async def drivers_endpoint():
    list_of_drivers = await fetch_drivers()
    return list(list_of_drivers.values())

@app.get('/results/{year}/{country}/', response_model=list[RaceResult])
async def race_results_endpoint(year: int = Path(..., ge=2023, le=2025), country: str = Path(...)):
    return await get_race_results(year, country)
    
@app.get('/standings/{year}/', response_model=list[StandingsEntry])
async def standings_endpoint(
    year: int = Path(
        ..., ge=2023, le=2025,
        description="Rok musi być pomiędzy 2023 a 2025"
        )
    ):
    return await get_standings(year)

    

    
    
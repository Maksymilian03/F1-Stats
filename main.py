from fastapi import FastAPI, HTTPException
from schemas import Driver, RaceResult
import httpx
from services import fetch_drivers




app = FastAPI()


@app.get("/")
def root():
    return {"message": "F1 Stats"}


@app.get('/drivers/', response_model=list[Driver])
async def get_drivers():
    list_of_drivers = await fetch_drivers()
    return (list(list_of_drivers.values()))

@app.get('/results/{year}/{country}/', response_model=list[RaceResult])
async def get_race_results(year: int, country: str):
    url_session = f'https://api.openf1.org/v1/sessions?country_name={country}&session_name=Race&year={year}'
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url_session)
        print(response.json())
        if 'detail' in response.json():
            raise HTTPException(status_code=404, detail='Nie znaleziono wyścigu')
        session_key = response.json()[0]['session_key']
        list_of_drivers = await fetch_drivers(session_key)
        url_results = f'https://api.openf1.org/v1/session_result?session_key={session_key}'
        response2 = await client.get(url_results)
        final_list = []
        for result in response2.json():
           result['full_name'] = list_of_drivers[result['driver_number']]['full_name']
           final_list.append(result)

        return final_list

    

    
    
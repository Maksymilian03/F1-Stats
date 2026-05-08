import httpx
from fastapi import FastAPI, HTTPException
import asyncio


RACE_POINTS = {
    1: 25,
    2: 18,
    3: 15,
    4: 12,
    5: 10,
    6: 8,
    7: 6,
    8: 4,
    9: 2,
    10: 1
}

SPRINT_POINTS = {
    1: 8,
    2: 7,
    3: 6,
    4: 5,
    5: 4,
    6: 3,
    7: 2,
    8: 1
}


async def fetch_drivers(session_key='latest') -> dict[int, dict]:
    url = f'https://api.openf1.org/v1/drivers?session_key={session_key}'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    list_of_drivers = {driver['driver_number']: driver for driver in response.json()} 

    return list_of_drivers

async def get_races_and_sprints(year: int) ->tuple[list[int], list[int]]:
    """
    Funkcja pobierze wszytskie wyscigi i sprinty
    z danego roku i zwroci w dwoch listach ich klucze sesji 
    pierwsza zwrocona lista to klucze wyscigów a druga to klucze sprintów
    """
    race_url = f'https://api.openf1.org/v1/sessions?year={year}&session_name=Race'
    sprint_url = f'https://api.openf1.org/v1/sessions?year={year}&session_name=Sprint'
    try:
        async with httpx.AsyncClient() as client:
            race_response, sprint_response= await asyncio.gather(client.get(race_url), client.get(sprint_url))
            race_response.raise_for_status()
            sprint_response.raise_for_status()
            if isinstance(race_response.json(), dict) and 'detail' in race_response.json():
                raise HTTPException(status_code=404, detail='Nie znaleziono wyscigów')
            if isinstance(sprint_response.json(), dict) and 'detail' in sprint_response.json():
                raise HTTPException(status_code=404, detail='Nie znaleziono sprintów')
            race_keys = [session['session_key'] for session in race_response.json()]
            sprint_keys = [session['session_key'] for session in sprint_response.json()]
    except httpx.HTTPStatusError as e:
        raise (HTTPException(status_code=502, detail=f'OpenF1 Api error: {e}'))
    except httpx.RequestError as e:
        raise (HTTPException(status_code=503, detail=f'Błąd połączenia: {e}'))
    else:
        return race_keys, sprint_keys



async def fetch_session_results(session_key: int) -> list[dict]:
    """
    Funkcja na podstawie klucza sesesji zrwoci wynik tej sesji
    """
    url = f'https://api.openf1.org/v1/session_result?session_key={session_key}'
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, dict) and 'detail' in data:
                raise HTTPException(status_code=404, detail='Nie znaleziono sesji')
        
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f'OpenF1 Api error: {e}')
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f'Błąd połączenia: {e}')
    else:
        return data
    
    

def calculate_points(all_session_results: list[list[dict]], points_table: dict[int, int]) -> dict[int, dict]:
    """
    Funkcja zliczy ilość punktów dla kierowcy
    i ilosc zwyciest w wyscigach i zwroci to w postaci:
    {44: {'points': 222, 'wins': 2}}, {55: {'points': 45, 'wins': 1}
    """
    pass

def merge_driver_details(list_of_drivers: dict[int, dict], standings_data: dict) -> dict:
    """
    Funkcja doda do driver_data liczbe punktow kierowcy
    oraz ilosc wygranych wyscigów i zwroci słownik gdzie
    kluczem bedzie numer kierowcy a wartoscia pozostałe informacje
    """
    pass

def leaderboard(list_of_drivers_with_points: dict) -> list:
    """
    Funkcja posegreguje kierowcow po ilosci ich punktów od najwiekszej
    do najmniejszej jesli kierowcy maja tyle samo punktow 
    to pod uwage bedzie brana ilosc zwyciestw w wyscigach
    i zwroci liste kierowcow posortowana od najwiekszej do najmniejszej
    """
    pass

async def get_standings(year: int) -> list[dict]:
    """
    Funkcja wywoła wszytskie potrzbne funkcje zeby zwrocic klasyfikacje w danym sezonie
    """
    pass
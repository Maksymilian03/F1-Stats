import httpx
from fastapi import FastAPI, HTTPException
import asyncio
import os
import json
import time
import datetime


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

CACHE_DIR = 'cache'
CACHE_TTL_SECONDS = 3600


async def fetch_drivers(session_key='latest') -> dict[int, dict]:
    url = f'https://api.openf1.org/v1/drivers?session_key={session_key}'
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            data = response.json()
            if isinstance(data, dict) and 'detail' in data:
                raise HTTPException(status_code=404, detail='Nie znaleziono kierowców')
    
        list_of_drivers = {driver['driver_number']: driver for driver in response.json()} 

        return list_of_drivers
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f'OpenF1 Api error: {e}')
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f'Błąd połączenia: {e}')

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
            race_response, sprint_response = await asyncio.gather(client.get(race_url), client.get(sprint_url))
            race_response.raise_for_status()
            sprint_response.raise_for_status()

            race_data = race_response.json()
            sprint_data = sprint_response.json()    

            if isinstance(race_data, dict) and 'detail' in race_data:
                raise HTTPException(status_code=404, detail='Nie znaleziono wyscigów')
            if isinstance(sprint_data, dict) and 'detail' in sprint_data:
                raise HTTPException(status_code=404, detail='Nie znaleziono sprintów')
            
            race_keys = [session['session_key'] for session in  race_data]
            sprint_keys = [session['session_key'] for session in sprint_data]

            return race_keys, sprint_keys
        
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f'OpenF1 Api error: {e}')
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f'Błąd połączenia: {e}')



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
            return data
    
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f'OpenF1 Api error: {e}')
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f'Błąd połączenia: {e}')


    

def calculate_points(all_session_results: list[list[dict]], points_table: dict[int, int], count_wins: bool = True) -> dict[int, dict]:
    """
    Funkcja zliczy ilość punktów dla kierowcy
    i ilosc zwyciest w wyscigach i zwroci to w postaci:
    {44: {'points': 222, 'wins': 2}}, {55: {'points': 45, 'wins': 1}
    """
    result = {}
    for session_result in all_session_results:
        for driver_result in session_result:
            driver_number, position = driver_result['driver_number'], driver_result['position']
            if driver_number not in result:
                result[driver_number] = {'points': 0, 'wins': 0}
            
            result[driver_number]['points'] += points_table.get(position, 0)
            if count_wins and position == 1:
                result[driver_number]['wins'] += 1
    return result


def merge_driver_details(list_of_drivers: dict[int, dict], standings_data: dict) -> dict:
    """
    Funkcja doda do driver_data liczbe punktow kierowcy
    oraz ilosc wygranych wyscigów i zwroci słownik gdzie
    kluczem bedzie numer kierowcy a wartoscia pozostałe informacje
    """
    list_of_merge_drivers = {}
    for driver_number, stats in standings_data.items():
        
        points = stats['points']
        wins = stats['wins']
        driver_info = list_of_drivers.get(driver_number)

        if driver_info is None:
            full_name = "Unknown"
            team = "Unknown"
        else:
            full_name = driver_info['full_name']
            team = driver_info['team_name']

        list_of_merge_drivers[driver_number] = {
            'driver_number': driver_number,
            'full_name': full_name,
            'team': team,
            'points': points,
            'wins': wins
        }
    return list_of_merge_drivers




def leaderboard(list_of_drivers_with_points: dict) -> list:
    """
    Funkcja posegreguje kierowcow po ilosci ich punktów od najwiekszej
    do najmniejszej jesli kierowcy maja tyle samo punktow 
    to pod uwage bedzie brana ilosc zwyciestw w wyscigach
    i zwroci liste kierowcow posortowana od najwiekszej do najmniejszej
    """
    leaderboard_list = sorted(list_of_drivers_with_points.values(), key=lambda x: (x['points'], x['wins']), reverse=True)

    for index, driver in enumerate(leaderboard_list):
        driver['position'] = index + 1
    return leaderboard_list
        

async def fetch_session_with_semaphore(semphory: asyncio.Semaphore, session_key: int) -> list[dict]:
    """
    Funkcja opakowuje fetch_session_results w semafor zeby ograniczyc ilosc jednoczesnych polaczen do api
    """
    async with semphory:
        await asyncio.sleep(2)  # Dodajemy małe opóźnienie, aby rozłożyć żądania w czasie
        return await fetch_session_results(session_key)

async def get_standings(year: int) -> list[dict]:
    """
    Funkcja wywoła wszytskie potrzbne funkcje zeby zwrocic klasyfikacje w danym sezonie
    """
    # Odczyt z cache
    cache_path = os.path.join(CACHE_DIR, f'standings_{year}.json')  
    if os.path.exists(cache_path):
        if year < datetime.datetime.now().year:
            with open(cache_path, 'r') as f:
                return json.load(f)
        elif year == datetime.datetime.now().year:
            cache_mtime = os.path.getmtime(cache_path)
            if time.time() - cache_mtime < CACHE_TTL_SECONDS:
                with open(cache_path, 'r') as f:
                    return json.load(f)

    race_keys, sprint_keys = await get_races_and_sprints(year)

    semaphore = asyncio.Semaphore(2)

    race_results, sprint_results, list_of_drivers = await asyncio.gather(
        asyncio.gather(*[fetch_session_with_semaphore(semaphore, key) for key in race_keys]),
        asyncio.gather(*[fetch_session_with_semaphore(semaphore, key) for key in sprint_keys]),
        fetch_drivers(session_key=race_keys[-1])
    )

    race_points = calculate_points(race_results, RACE_POINTS, count_wins=True)
    sprint_points = calculate_points(sprint_results, SPRINT_POINTS, count_wins=False)


    combined = {}
    all_drivers = set(race_points.keys()).union(sprint_points.keys())
    for driver_number in all_drivers:
        race_stats = race_points.get(driver_number, {'points': 0, 'wins': 0})
        sprint_stats = sprint_points.get(driver_number, {'points': 0, 'wins': 0})
        combined[driver_number] = {
            'points': race_stats['points'] + sprint_stats['points'],
            'wins': race_stats['wins'] + sprint_stats['wins']
        }

    drivers_with_points = merge_driver_details(list_of_drivers, combined)

    result = leaderboard(drivers_with_points)

    # Zapis do cache
    os.makedirs(CACHE_DIR, exist_ok=True)  
    with open(cache_path, 'w') as f:
        json.dump(result, f)

    return result
    

    
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

CURRENT_YEAR = datetime.datetime.now().year

CACHE_DIR = 'cache'
CACHE_TTL_SECONDS = 3600


async def _fetch_openf1(url: str, not_found_message: str) -> list | dict:
    """
    Funkcja pomocnicza do pobierania danych z OpenF1 API z obsługą błędów
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, dict) and 'detail' in data:
                raise HTTPException(status_code=404, detail=not_found_message)
            return data
    
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f'OpenF1 Api error: {e}')
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f'Błąd połączenia: {e}')

async def fetch_drivers(session_key='latest') -> dict[int, dict]:
    """
    Funkcja pobierze wszystkich kierowców z OpenF1 API i zwróci
    słownik gdzie kluczem jest numer kierowcy a wartością pozostałe informacje o nim
    """
    url = f'https://api.openf1.org/v1/drivers?session_key={session_key}'
    data = await _fetch_openf1(url, 'Nie znaleziono kierowców')
    return {driver['driver_number']: driver for driver in data}

async def get_race_results(year: int, country: str) -> list[dict]:
    """
    Funkcja pobierze wyniki wyscigu z danego roku i kraju i zwroci liste wyników z dodanym imieniem i nazwiskiem kierowcy
    """
    url_session = f'https://api.openf1.org/v1/sessions?country_name={country}&session_name=Race&year={year}'
    data = await _fetch_openf1(url_session, 'Nie znaleziono wyścigu')
    if not data:
        raise HTTPException(status_code=404, detail='Nie znaleziono wyścigu')
    session_key = data[0]['session_key']

    drivers, results = await asyncio.gather(
        fetch_drivers(session_key),
        fetch_session_results(session_key)
    )
    for result in results:
        result['full_name'] = drivers[result['driver_number']]['full_name']
    return results



async def get_races_and_sprints(year: int) ->tuple[list[int], list[int]]:
    """
    Funkcja pobierze wszytskie wyscigi i sprinty
    z danego roku i zwroci w dwoch listach ich klucze sesji 
    pierwsza zwrocona lista to klucze wyscigów a druga to klucze sprintów
    """
    race_url = f'https://api.openf1.org/v1/sessions?year={year}&session_name=Race'
    sprint_url = f'https://api.openf1.org/v1/sessions?year={year}&session_name=Sprint'
    race_session, sprint_session = await asyncio.gather(
        _fetch_openf1(race_url, 'Nie znaleziono wyscigów'),
        _fetch_openf1(sprint_url, 'Nie znaleziono sprintów')
    )
    race_keys = [session['session_key'] for session in race_session]
    sprint_keys = [session['session_key'] for session in sprint_session]
    return race_keys, sprint_keys

async def fetch_session_results(session_key: int) -> list[dict]:
    """
    Funkcja na podstawie klucza sesesji zrwoci wynik tej sesji
    """
    url = f'https://api.openf1.org/v1/session_result?session_key={session_key}'
    return await _fetch_openf1(url, 'Nie znaleziono wyników sesji')

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


def aggregate_points_by_team(drivers_with_points: dict[int, dict], drivers_info: dict[int, dict]) -> dict[str, dict]:
    """
    Funkcja zliczy punkty dla kazdego teamu i zwroci słownik gdzie kluczem bedzie nazwa teamu a wartoscia
    będzie słownik z kluczami 'points' i 'wins' z sumą punktów i zwyciestw dla kierowców tego teamu
    """
    
    team_points = {}
    for driver_number, stats in drivers_with_points.items():
        driver_info = drivers_info.get(driver_number)
        if driver_info is None:
            continue
        team = driver_info['team_name']
        if team is None:
            continue
        if team not in team_points:
            team_points[team] = {'team': team, 'points': 0, 'wins': 0}
        team_points[team]['points'] += stats['points']
        team_points[team]['wins'] += stats['wins']
    return team_points
   
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
        

async def fetch_session_with_semaphore(semaphore: asyncio.Semaphore, session_key: int) -> list[dict]:
    """
    Funkcja opakowuje fetch_session_results w semafor zeby ograniczyc ilosc jednoczesnych polaczen do api
    """
    async with semaphore:
        await asyncio.sleep(2)  # Dodajemy małe opóźnienie, aby rozłożyć żądania w czasie
        return await fetch_session_results(session_key)

async def get_driver_standings(year: int) -> list[dict]:
    """
    Funkcja wywoła wszytskie potrzbne funkcje zeby zwrocic klasyfikacje w danym sezonie
    """
    # Odczyt z cache
    cache_path = os.path.join(CACHE_DIR, f'drivers_standings_{year}.json')  
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

    semaphore = asyncio.Semaphore(1)

    if not race_keys:
        return []
    
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
    

    
async def get_constructor_standings(year: int) -> list[dict]:
    """
    Funkcja zwroci klasyfikacje konstruktorów w danym sezonie
    """
    # Odczyt z cache
    cache_path = os.path.join(CACHE_DIR, f'constructor_standings_{year}.json')  
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

    semaphore = asyncio.Semaphore(1)

    if not race_keys:
        return []

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

    teams = aggregate_points_by_team(combined, list_of_drivers)

    result = leaderboard(teams)

    # Zapis do cache
    os.makedirs(CACHE_DIR, exist_ok=True)  
    with open(cache_path, 'w') as f:
        json.dump(result, f)

    return result
    
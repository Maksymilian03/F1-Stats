from unittest.mock import AsyncMock, patch
from models import DriverStanding
from sqlalchemy import func, select


@patch("services.get_races_and_sprints", new_callable=AsyncMock)
async def test_get_driver_standings_returns_empty_list_when_no_races(
    mock_get_races_and_sprints, client
):
    # Arrange
    mock_get_races_and_sprints.return_value = ([], [])

    # Act
    response = await client.get("/standings/2023/")

    # Assert
    assert response.status_code == 200
    assert response.json() == []
    mock_get_races_and_sprints.assert_called_once_with(2023)


async def test_get_driver_standings_returns_data_from_db_when_cache_is_fresh(client, db_session):
    # Arrange
    year = 2024
    verstappen = DriverStanding(
        year=year,
        position=1,
        driver_number=1,
        full_name="Max Verstappen",
        team="Red Bull",
        points=437,
        wins=15,
)
    hamilton = DriverStanding(
        year=year,
        position=2,
        driver_number=44,
        full_name="Lewis Hamilton",
        team="Mercedes",
        points=190,
        wins=2,
)
    db_session.add_all([verstappen, hamilton])
    await db_session.commit()

    # Act 
    response = await client.get(f"/standings/{year}/")

    # Assert
    assert response.status_code == 200
    assert response.json() == [
    {"position": 1, "driver_number": 1, "full_name": "Max Verstappen", "team": "Red Bull", "points": 437, "wins": 15},
    {"position": 2, "driver_number": 44, "full_name": "Lewis Hamilton", "team": "Mercedes", "points": 190, "wins": 2},
]
    

@patch('services.get_races_and_sprints', new_callable=AsyncMock)
@patch('services.fetch_session_with_semaphore', new_callable=AsyncMock)
@patch('services.fetch_drivers', new_callable=AsyncMock)  
async def test_get_driver_standings_fetches_from_openf1_and_saves_to_db_when_cache_miss(
    mock_fetch_drivers, mock_fetch_session_with_semaphore, mock_get_races_and_sprints, client, db_session,
    fake_drivers, fake_race_keys, fake_sprint_keys, fake_races_results, fake_sprints_results
):
    # Arange 
    year = 2024

    expected_driver_standings =[
    {"position": 1, "driver_number": 3,  "full_name": "Max Verstappen",   "team": "Red Bull",  "points": 90, "wins": 2},
    {"position": 2, "driver_number": 44, "full_name": "Lewis Hamilton",   "team": "Mercedes",  "points": 79, "wins": 1},
    {"position": 3, "driver_number": 16, "full_name": "Charles Leclerc",  "team": "Ferrari",   "points": 68, "wins": 0},
    {"position": 4, "driver_number": 6,  "full_name": "Sergio Perez",     "team": "Red Bull",  "points": 51, "wins": 0},
    {"position": 5, "driver_number": 45, "full_name": "Carlos Sainz",     "team": "Ferrari",   "points": 42, "wins": 0},
    {"position": 6, "driver_number": 77, "full_name": "Valtteri Bottas",  "team": "Mercedes",  "points": 33, "wins": 0},
]
    
    mock_get_races_and_sprints.return_value = (fake_race_keys, fake_sprint_keys)
    mock_fetch_session_with_semaphore.side_effect = fake_races_results + fake_sprints_results
    mock_fetch_drivers.return_value = fake_drivers

    # Act
    response = await client.get(f"/standings/{year}/")

    # Assert
    assert response.status_code == 200
    assert response.json() == expected_driver_standings

    stmt = select(DriverStanding).where(DriverStanding.year == year)
    result = await db_session.execute(stmt)
    saved_records = result.scalars().all()
    assert len(saved_records) == 6

    mock_get_races_and_sprints.assert_called_once_with(year)

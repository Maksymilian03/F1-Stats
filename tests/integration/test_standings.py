from unittest.mock import AsyncMock, patch
from models import DriverStanding



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
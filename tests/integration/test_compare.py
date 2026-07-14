from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from main import app
from schemas import DriverStandingInfo
from database import get_db


client = TestClient(app)

@patch('services.load_comparison_data_from_db', new_callable=AsyncMock)
@patch('services.get_driver_standings', new_callable=AsyncMock)
def test_compare_endpoint_returns_200_with_full_response(mock_get_driver_standings, mock_load_comparison_data_from_db, override_get_db):
    # Arrange 
   

    mock_load_comparison_data_from_db.return_value = (
        DriverStandingInfo(position=1, full_name="Max Verstappen", driver_number=1, team="Red Bull", points=100, wins=3),
        DriverStandingInfo(position=2, full_name="Lando Norris", driver_number=4, team="McLaren", points=80, wins=2)
    )  

    # Act
    response = client.get("/compare/2024/1/4/")

    # Assert
    mock_get_driver_standings.assert_awaited_once()
    mock_load_comparison_data_from_db.assert_awaited_once()
    assert response.status_code == 200
    assert response.json() == {
        "driver1": {
            "position": 1,
            "full_name": "Max Verstappen",
            "driver_number": 1,
            "team": "Red Bull",
            "points": 100,
            "wins": 3
        },
        "driver2": {
            "position": 2,
            "full_name": "Lando Norris",
            "driver_number": 4,
            "team": "McLaren",
            "points": 80,
            "wins": 2
        },
        "comparison": {
            "points_difference": 20,
            "wins_difference": 1,
            "position_difference": 1,
            "leader": {
                "position": 1,
                "full_name": "Max Verstappen",
                "driver_number": 1,
                "team": "Red Bull",
                "points": 100,
                "wins": 3
            }
        }
    }


def test_compare_endpoint_returns_400_when_driver_numbers_are_equal(override_get_db):
    # Arrange
    year = 2023
    driver1_number = 3
    driver2_number = 3

    # Act
    response = client.get(f'/compare/{year}/{driver1_number}/{driver2_number}/')

    # Assert
    assert response.status_code == 400


def test_compare_endpoint_returns_422_when_driver_number_is_zero(override_get_db):
    # Arrange
    year = 2023
    driver1_number = 3

    # Act
    response = client.get(f'/compare/{year}/{driver1_number}/0/')

    # Assert
    assert response.status_code == 422


def test_compare_endpoint_returns_422_when_year_is_before_2023(override_get_db):
    # Arrange
    year = 2022
    driver1_number = 3
    driver2_number = 44

    # Act
    response = client.get(f'/compare/{year}/{driver1_number}/{driver2_number}/')

    # Assert
    assert response.status_code == 422

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from main import app
from services import CURRENT_YEAR, get_constructor_standings


@pytest.mark.asyncio
@patch('services.get_races_and_sprints')
@patch('services.fetch_session_with_semaphore')
@patch('services.fetch_drivers')
async def test_get_constructor_standings_returns_correct_position(drivers_mock, session_mock, races_and_sprints_mock,
     tmp_path, monkeypatch, fake_drivers, fake_sprints_results, fake_races_results, fake_race_keys, fake_sprint_keys):

    # Arrange
    monkeypatch.setattr('services.CACHE_DIR', str(tmp_path))

    drivers_mock.return_value = fake_drivers
    races_and_sprints_mock.return_value = (fake_race_keys, fake_sprint_keys)
    session_mock.side_effect = fake_races_results + fake_sprints_results

    # Act
    result = await get_constructor_standings(2023)

    # Assert
    assert result[0]['team'] == "Red Bull"
    assert result[1]['team'] == "Mercedes"
    assert result[2]['team'] == "Ferrari"

@pytest.mark.asyncio
@patch('services.get_races_and_sprints')
@patch('services.fetch_session_with_semaphore')
@patch('services.fetch_drivers')
async def test_get_constructor_standings_calculates_total_points_correctly(drivers_mock, session_mock, races_and_sprints_mock,
         tmp_path, monkeypatch, fake_drivers, fake_sprints_results, fake_races_results, fake_race_keys, fake_sprint_keys):

    # Arrange
    monkeypatch.setattr('services.CACHE_DIR', str(tmp_path))

    drivers_mock.return_value = fake_drivers
    races_and_sprints_mock.return_value = (fake_race_keys, fake_sprint_keys)
    session_mock.side_effect = fake_races_results + fake_sprints_results

    # Act
    result = await get_constructor_standings(2023)

    # Assert
    max_verstappen_points = (25 + 18 + 25 + 8 + 7 + 7)
    sergio_perez_points = (12 + 12 + 12 + 5 + 5 + 5)
    red_bull_points = max_verstappen_points + sergio_perez_points

    lewis_hamilton_points = (18 + 25 + 15 + 7 + 8 + 6)
    valtteri_bottas_points = (8 + 8 + 8 + 3 + 3 + 3)
    mercedes_points = lewis_hamilton_points + valtteri_bottas_points

    charles_leclerc_points = (15 + 15 + 18 + 6 + 6 + 8)
    carlos_sainz_points = (10 + 10 + 10 + 4 + 4 + 4)
    ferrari_points = charles_leclerc_points + carlos_sainz_points

    assert result[0]['points'] == red_bull_points
    assert result[1]['points'] == mercedes_points
    assert result[2]['points'] == ferrari_points

@pytest.mark.asyncio
@patch('services.get_races_and_sprints')
@patch('services.fetch_session_with_semaphore')
@patch('services.fetch_drivers')
async def test_get_constructor_standings_does_not_count_sprint_wins_as_total_wins(drivers_mock, session_mock, races_and_sprints_mock,
         tmp_path, monkeypatch, fake_drivers, fake_sprints_results, fake_races_results, fake_race_keys, fake_sprint_keys):

    # Arrange
    monkeypatch.setattr('services.CACHE_DIR', str(tmp_path))

    drivers_mock.return_value = fake_drivers
    races_and_sprints_mock.return_value = (fake_race_keys, fake_sprint_keys)
    session_mock.side_effect = fake_races_results + fake_sprints_results

    # Act
    result = await get_constructor_standings(2023)

    # Assert

    max_verstappen_wins = 2
    sergio_perez_wins = 0
    red_bull_wins = max_verstappen_wins + sergio_perez_wins

    lewis_hamilton_wins = 1
    valtteri_bottas_wins = 0
    mercedes_wins = lewis_hamilton_wins + valtteri_bottas_wins

    charles_leclerc_wins = 0
    carlos_sainz_wins = 0
    ferrari_wins = charles_leclerc_wins + carlos_sainz_wins

    assert result[0]['wins'] == red_bull_wins
    assert result[1]['wins'] == mercedes_wins
    assert result[2]['wins'] == ferrari_wins


@pytest.mark.asyncio
@patch('services.get_races_and_sprints')
async def test_get_constructor_standings_returns_empty_list_when_no_races_or_sprints(races_and_sprints_mock,
                                                                                      tmp_path, monkeypatch):
    # Arrange
    monkeypatch.setattr('services.CACHE_DIR', str(tmp_path))

    races_and_sprints_mock.return_value = ([], [])

    # Act
    result = await get_constructor_standings(2026)

    # Assert
    assert result == []


client = TestClient(app)
def test_get_constructor_standings_raise_422_when_year_is_less_than_2023():
    # Arrange
    year = 2000

    # Act
    response = client.get(f"/standings/constructors/{year}/")

    # Assert
    assert response.status_code == 422

def test_get_constructor_standings_raise_422_when_year_is_greater_than_current_year():
    # Arrange
    year = CURRENT_YEAR + 1

    # Act
    response = client.get(f"/standings/constructors/{year}/")

    # Assert
    assert response.status_code == 422



import json
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from main import app
from services import CURRENT_YEAR, get_driver_standings


@pytest.mark.asyncio
@patch('services.get_races_and_sprints')
@patch('services.fetch_session_with_semaphore')
@patch('services.fetch_drivers')
async def test_get_driver_standings_returns_correct_position(drivers_mock, session_mock, races_and_sprints_mock,
     tmp_path, monkeypatch, fake_drivers, fake_sprints_results, fake_races_results, fake_race_keys, fake_sprint_keys):
    # Arrange
    monkeypatch.setattr('services.CACHE_DIR', str(tmp_path))

    drivers_mock.return_value = fake_drivers
    races_and_sprints_mock.return_value = (fake_race_keys, fake_sprint_keys)
    session_mock.side_effect = fake_races_results + fake_sprints_results

    # Act
    result = await get_driver_standings(2023)

    # Assert

    assert result[0]['driver_number'] == 3
    assert result[1]['driver_number'] == 44
    assert result[2]['driver_number'] == 16


@pytest.mark.asyncio
@patch('services.get_races_and_sprints')
@patch('services.fetch_session_with_semaphore')
@patch('services.fetch_drivers')
async def test_get_driver_standings_calculates_total_points_correctly(drivers_mock, session_mock, races_and_sprints_mock,
         tmp_path, monkeypatch, fake_drivers, fake_sprints_results, fake_races_results, fake_race_keys, fake_sprint_keys):
    # Arrange
    monkeypatch.setattr('services.CACHE_DIR', str(tmp_path))

    drivers_mock.return_value = fake_drivers
    races_and_sprints_mock.return_value = (fake_race_keys, fake_sprint_keys)
    session_mock.side_effect = fake_races_results + fake_sprints_results

    # Act
    result = await get_driver_standings(2023)

    # Assert

    assert result[0]['points'] == 25 + 18 + 25 + 8 + 7 + 7
    assert result[1]['points'] == 18 + 25 + 15 + 7 + 8 + 6
    assert result[2]['points'] == 15 + 15 + 18 + 6 + 6 + 8


@pytest.mark.asyncio
@patch('services.get_races_and_sprints')
@patch('services.fetch_session_with_semaphore')
@patch('services.fetch_drivers')
async def test_get_driver_standings_does_not_count_sprint_wins_as_total_wins(drivers_mock, session_mock,
     races_and_sprints_mock, tmp_path, monkeypatch, fake_drivers, fake_sprints_results,
       fake_races_results, fake_race_keys, fake_sprint_keys):
    # Arrange
    monkeypatch.setattr('services.CACHE_DIR', str(tmp_path))

    drivers_mock.return_value = fake_drivers
    races_and_sprints_mock.return_value = (fake_race_keys, fake_sprint_keys)
    session_mock.side_effect = fake_races_results + fake_sprints_results

    # Act
    result = await get_driver_standings(2023)

    # Assert

    assert result[0]['wins'] == 1 + 0 + 1 + 0 + 0 + 0
    assert result[1]['wins'] == 0 + 1 + 0 + 0 + 0 + 0
    assert result[2]['wins'] == 0 + 0 + 0 + 0 + 0 + 0

@pytest.mark.asyncio
@patch('services.get_races_and_sprints')
@patch('services.fetch_session_with_semaphore')
@patch('services.fetch_drivers')
async def test_get_driver_standings_returns_all_drivers_with_cached_data(drivers_mock, session_mock,
                                     races_and_sprints_mock, tmp_path, monkeypatch, fake_cached_data):
    # Arrange
    year = 2023
    monkeypatch.setattr('services.CACHE_DIR', str(tmp_path))

    cache_file = tmp_path / f'drivers_standings_{year}.json'

    cache_file.write_text(json.dumps(fake_cached_data))

    # Act
    result = await get_driver_standings(year)

    # Assert
    assert result == fake_cached_data
    drivers_mock.assert_not_called()
    session_mock.assert_not_called()
    races_and_sprints_mock.assert_not_called()

@pytest.mark.asyncio
@patch('services.get_races_and_sprints')
async def test_get_driver_standings_returns_empty_list_when_no_races_or_sprints(
     races_and_sprints_mock, tmp_path, monkeypatch):
    # Arrange
    year = 2026
    monkeypatch.setattr('services.CACHE_DIR', str(tmp_path))

    races_and_sprints_mock.return_value = ([], [])

    # Act
    result = await get_driver_standings(year)

    # Assert
    assert result == []

client = TestClient(app)
def test_get_driver_standings_raise_422_when_year_is_less_than_2023():
    # Arrange
    year = 2000


    # Act
    response = client.get(f'/standings/{year}/')

    # Assert
    assert response.status_code == 422
    assert "detail" in response.json()

def test_get_driver_standings_raise_422_when_year_is_greater_than_current_year():
    # Arrange
    year = CURRENT_YEAR + 1

    # Act
    response = client.get(f'/standings/{year}/')

    # Assert
    assert response.status_code == 422
    assert "detail" in response.json()

from unittest.mock import patch
import pytest, json

from services import get_driver_standings

@pytest.mark.asyncio
@patch('services.get_races_and_sprints')
@patch('services.fetch_session_with_semaphore')
@patch('services.fetch_drivers')
async def test_get_driver_standings_returns_all_drivers(drivers_mock, session_mock, races_and_sprints_mock, tmp_path, monkeypatch):
    # Arrange
    monkeypatch.setattr('services.CACHE_DIR', str(tmp_path))
    
    fake_race_keys = [9575, 9573, 9572]
    fake_sprint_keys = [9579, 9888, 9571]

    fake_races_results = [
    [{"position": 1, "driver_number": 3, "points": 25, "session_key": 9575},
        {"position": 2, "driver_number": 44, "points": 18, "session_key": 9575},
        {"position": 3, "driver_number": 16, "points": 15, "session_key": 9575}],
    [{"position": 1, "driver_number": 44, "points": 25, "session_key": 9573},
        {"position": 2, "driver_number": 3, "points": 18, "session_key": 9573},
        {"position": 3, "driver_number": 16, "points": 15, "session_key": 9573}],
    [{"position": 1, "driver_number": 3, "points": 25, "session_key": 9572},
        {"position": 2, "driver_number": 16, "points": 18, "session_key": 9572},
        {"position": 3, "driver_number": 44, "points": 15, "session_key": 9572}]    
    ]
    fake_sprints_results = [
  [{"position": 1, "driver_number": 3, "points": 8, "session_key": 9579},
    {"position": 2, "driver_number": 44, "points": 7, "session_key": 9579},
    {"position": 3, "driver_number": 16, "points": 6, "session_key": 9579}],
  [{"position": 1, "driver_number": 44, "points": 8, "session_key": 9888},
    {"position": 2, "driver_number": 3, "points": 7, "session_key": 9888},
    {"position": 3, "driver_number": 16, "points": 6, "session_key": 9888}],
  [{"position": 1, "driver_number": 16, "points": 8, "session_key": 9571},
    {"position": 2, "driver_number": 3, "points": 7, "session_key": 9571},
    {"position": 3, "driver_number": 44, "points": 6, "session_key": 9571}]
  ]
    

    fake_drivers = {
        44: {"driver_number": 44, "full_name": "Lewis Hamilton", "team_name": "Mercedes"},
        3: {"driver_number": 3, "full_name": "Max Verstappen", "team_name": "Red Bull"},
        16: {"driver_number": 16, "full_name": "Charles Leclerc", "team_name": "Ferrari"}
    }

    
    drivers_mock.return_value = fake_drivers
    races_and_sprints_mock.return_value = (fake_race_keys, fake_sprint_keys)
    session_mock.side_effect = fake_races_results + fake_sprints_results

    #ACT
    result = await get_driver_standings(2023)

    # ASSERT
    assert len(result) == 3

    assert result[0]['driver_number'] == 3
    assert result[0]['full_name'] == "Max Verstappen"
    assert result[0]['points'] == 25 + 18 + 25 + 8 + 7 + 7
    assert result[0]['wins'] == 1 + 0 + 1 + 0 + 0 + 0

    assert result[1]['driver_number'] == 44
    assert result[1]['full_name'] == "Lewis Hamilton"  
    assert result[1]['points'] == 18 + 25 + 15 + 7 + 8 + 6
    assert result[1]['wins'] == 0 + 1 + 0 + 0 + 0 + 0
    
    assert result[2]['driver_number'] == 16
    assert result[2]['full_name'] == "Charles Leclerc"
    assert result[2]['points'] == 15 + 15 + 18 + 6 + 6 + 8
    assert result[2]['wins'] == 0 + 0 + 0 + 0 + 0 + 0

@pytest.mark.asyncio
@patch('services.get_races_and_sprints')
@patch('services.fetch_session_with_semaphore')
@patch('services.fetch_drivers')
async def test_get_driver_standings_returns_all_drivers_with_cached_data(drivers_mock, session_mock, races_and_sprints_mock, tmp_path, monkeypatch):
    # Arrange
    year = 2023
    monkeypatch.setattr('services.CACHE_DIR', str(tmp_path))

    cache_file = tmp_path / f'drivers_standings_{year}.json'
    fake_cached_data = [
        {"driver_number": 3, "full_name": "Max Verstappen", "points": 100, "wins": 5},
        {"driver_number": 44, "full_name": "Lewis Hamilton", "points": 90, "wins": 4},
        {"driver_number": 16, "full_name": "Charles Leclerc", "points": 80, "wins": 3},
    ]

    cache_file.write_text(json.dumps(fake_cached_data))
    
    # Act
    result = await get_driver_standings(year)

    # Assert
    assert result == fake_cached_data
    drivers_mock.assert_not_called()
    session_mock.assert_not_called()
    races_and_sprints_mock.assert_not_called()
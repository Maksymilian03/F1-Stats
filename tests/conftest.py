import pytest

@pytest.fixture
def fake_drivers():
    return {
        44: {"driver_number": 44, "full_name": "Lewis Hamilton", "team_name": "Mercedes"},
        3: {"driver_number": 3, "full_name": "Max Verstappen", "team_name": "Red Bull"},
        16: {"driver_number": 16, "full_name": "Charles Leclerc", "team_name": "Ferrari"}
    }

@pytest.fixture
def fake_sprints_results():
    return [
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

@pytest.fixture
def fake_races_results():
    return [
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

@pytest.fixture
def fake_race_keys():
    return [9575, 9573, 9572]

@pytest.fixture
def fake_empty_race_keys():
    return []

@pytest.fixture
def fake_sprint_keys():
    return [9579, 9888, 9571]

@pytest.fixture
def fake_empty_sprint_keys():
    return []



@pytest.fixture
def fake_cached_data():
    return [
        {"driver_number": 3, "full_name": "Max Verstappen", "points": 100, "wins": 5},
        {"driver_number": 44, "full_name": "Lewis Hamilton", "points": 90, "wins": 4},
        {"driver_number": 16, "full_name": "Charles Leclerc", "points": 80, "wins": 3},
    ]
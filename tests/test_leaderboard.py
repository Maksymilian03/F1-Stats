import pytest
from services import leaderboard

def test_leaderboard_empty_input_returns_empty_list():
    drivers_with_points = {}

    result = leaderboard(drivers_with_points)

    assert result == []

def test_leaderboard_sorts_drivers_by_points_descending():
    data = {
        1:  {"driver_number": 1,  "points": 100, "wins": 5},
        44: {"driver_number": 44, "points": 200, "wins": 3},
        4:  {"driver_number": 4,  "points": 150, "wins": 2},
    }

    result = leaderboard(data)

    assert result[0]["points"] == 200
    assert result[1]["points"] == 150
    assert result[2]["points"] == 100

    assert result[0]["position"] == 1
    assert result[1]["position"] == 2
    assert result[2]["position"] == 3


def test_leaderboard_sorts_drivers_by_points_and_wins():
    data = {
        1:  {"driver_number": 1,  "points": 100, "wins": 5},
        44: {"driver_number": 44, "points": 100, "wins": 3},
        4:  {"driver_number": 4,  "points": 150, "wins": 2},
    }

    result = leaderboard(data)

    assert result[0]["points"] == 150
    assert result[1]["points"] == 100
    assert result[2]["points"] == 100

    assert result[0]['driver_number'] == 4
    assert result[1]['driver_number'] == 1
    assert result[2]['driver_number'] == 44


def test_leaderboard_preserves_team_data():
    data = {
        "McLaren":  {"team": "McLaren",  "points": 666, "wins": 6},
        "Ferrari":  {"team": "Ferrari",  "points": 652, "wins": 5},
    }

    result = leaderboard(data)

    assert result[0]["team"] == "McLaren"
    assert result[0]["points"] == 666
    assert result[0]["wins"] == 6
    assert result[1]["team"] == "Ferrari"
    assert result[1]["points"] == 652
    assert result[1]["wins"] == 5

    assert result[0]['position'] == 1
    assert result[1]['position'] == 2
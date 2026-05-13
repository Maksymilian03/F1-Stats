import pytest
from services import aggregate_points_by_team


def test_aggregate_points_by_team_sum_drivers_from_same_team():
    drivers_with_points = {
        1:  {"points": 50, "wins": 2},   # Verstappen
        11: {"points": 30, "wins": 0},   # Perez
    }

    drivers_info = {
        1:  {"driver_number": 1,  "full_name": "Max Verstappen", "team_name": "Red Bull Racing"},
        11: {"driver_number": 11, "full_name": "Sergio Perez",   "team_name": "Red Bull Racing"},
    }

    result = aggregate_points_by_team(drivers_with_points, drivers_info)

    assert result["Red Bull Racing"]["points"] == 50 + 30
    assert result["Red Bull Racing"]["wins"] == 2 + 0
    assert result["Red Bull Racing"]["team"] == "Red Bull Racing"


def test_aggregate_points_by_team_empty_input_returns_empty_dict():
    drivers_with_points = {}
    drivers_info = {}

    result = aggregate_points_by_team(drivers_with_points, drivers_info)

    assert result == {}


def test_aggregate_points_by_team_separates_different_teams():
    drivers_with_points = {
        1:  {"points": 50, "wins": 2},   # Red Bull
        44: {"points": 40, "wins": 1},   # Mercedes
        4:  {"points": 30, "wins": 0},   # McLaren
    }
    drivers_info = {
        1:  {"team_name": "Red Bull Racing"},
        44: {"team_name": "Mercedes"},
        4:  {"team_name": "McLaren"},
    }

    result = aggregate_points_by_team(drivers_with_points, drivers_info)

    assert len(result) == 3
    assert result["Red Bull Racing"]["points"] == 50
    assert result["Mercedes"]["points"] == 40
    assert result["McLaren"]["points"] == 30


def test_aggregate_points_by_team_with_missing_driver_info():
    drivers_with_points = {
        1:  {"points": 50, "wins": 2},   # Red Bull
        9:  {"points": 30, "wins": 1},   # McLaren
    }
    drivers_info = {
        1:  {"team_name": "Red Bull Racing"},
    }

    result = aggregate_points_by_team(drivers_with_points, drivers_info)

    assert len(result) == 1
    assert result["Red Bull Racing"]["points"] == 50
    assert result["Red Bull Racing"]["wins"] == 2


def test_aggregate_points_by_missing_team_name():
    drivers_with_points = {
        1:  {"points": 50, "wins": 2},   # Red Bull
        44: {"points": 40, "wins": 1},   # Mercedes
    }
    drivers_info = {
        1:  {"team_name": "Red Bull Racing"},
        44: {"team_name": None},  # Missing team name
    }

    result = aggregate_points_by_team(drivers_with_points, drivers_info)

    assert len(result) == 1
    assert result["Red Bull Racing"]["points"] == 50
    assert result["Red Bull Racing"]["wins"] == 2


def test_aggregate_points_by_team_sum_drivers_from_same_team_with_0_points():
    drivers_with_points = {
        1:  {"points": 0, "wins": 0},   # Verstappen
        11: {"points": 0, "wins": 0},   # Perez
    }

    drivers_info = {
        1:  {"driver_number": 1,  "full_name": "Max Verstappen", "team_name": "Red Bull Racing"},
        11: {"driver_number": 11, "full_name": "Sergio Perez",   "team_name": "Red Bull Racing"},
    }

    result = aggregate_points_by_team(drivers_with_points, drivers_info)

    assert result["Red Bull Racing"]["points"] == 0 + 0
    assert result["Red Bull Racing"]["wins"] == 0 + 0
    assert result["Red Bull Racing"]["team"] == "Red Bull Racing"

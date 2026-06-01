from services import merge_driver_details


def test_merge_driver_details_combines_points_and_info_for_one_driver():
    drivers_with_points = {
        1: {"points": 100, "wins": 5},
    }
    drivers_info = {
        1: {"full_name": "Max Verstappen", "team_name": "Red Bull Racing"},
    }

    result = merge_driver_details(drivers_info, drivers_with_points)

    assert result[1]["full_name"] == "Max Verstappen"
    assert result[1]["team"] == "Red Bull Racing"
    assert result[1]["points"] == 100
    assert result[1]["wins"] == 5
    assert result[1]["driver_number"] == 1


def test_merge_driver_details_empty_input_returns_empty_dict():
    drivers_with_points = {}
    drivers_info = {}

    result = merge_driver_details(drivers_info, drivers_with_points)

    assert result == {}

def test_merge_driver_details_with_missing_info():
    drivers_with_points = {
        1: {"points": 100, "wins": 5},
        44: {"points": 150, "wins": 3},
    }
    drivers_info = {
        1: {"full_name": "Max Verstappen", "team_name": "Red Bull Racing"},
    }

    result = merge_driver_details(drivers_info, drivers_with_points)

    assert result[1]["full_name"] == "Max Verstappen"
    assert result[1]["team"] == "Red Bull Racing"
    assert result[1]["points"] == 100
    assert result[1]["wins"] == 5
    assert result[1]["driver_number"] == 1

    assert result[44]["full_name"] == "Unknown"
    assert result[44]["team"] == "Unknown"
    assert result[44]["points"] == 150
    assert result[44]["wins"] == 3
    assert result[44]["driver_number"] == 44

def test_merge_driver_details_combines_points_and_info_for_each_driver():
    drivers_with_points = {
        1: {"points": 100, "wins": 5},
        44: {"points": 150, "wins": 3},
    }
    drivers_info = {
        1: {"full_name": "Max Verstappen", "team_name": "Red Bull Racing"},
        44: {"full_name": "Lewis Hamilton", "team_name": "Mercedes"},
    }

    result = merge_driver_details(drivers_info, drivers_with_points)

    assert result[1]["full_name"] == "Max Verstappen"
    assert result[1]["team"] == "Red Bull Racing"
    assert result[1]["points"] == 100
    assert result[1]["wins"] == 5
    assert result[1]["driver_number"] == 1

    assert result[44]["full_name"] == "Lewis Hamilton"
    assert result[44]["team"] == "Mercedes"
    assert result[44]["points"] == 150
    assert result[44]["wins"] == 3
    assert result[44]["driver_number"] == 44

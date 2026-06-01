from services import RACE_POINTS, calculate_points


def test_calculate_points_empty_input_returns_empty_dict():
    session = []

    result = calculate_points(session, RACE_POINTS)

    assert result == {}


def test_calculate_points_winner_gets_correct_stats():
    session = [
        [
            {"driver_number": 44, "position": 1},
        ]
    ]

    result = calculate_points(session, RACE_POINTS)

    assert result[44]["points"] == 25
    assert result[44]["wins"] == 1


def test_calculate_points_dnf_gets_zero_points():
    session = [
        [
            {"driver_number": 33, "position": None},
        ]
    ]

    result = calculate_points(session, RACE_POINTS)

    assert result[33]["points"] == 0
    assert result[33]["wins"] == 0


def test_calculate_points_outside_top_10_gets_zero_points():
    session = [
        [
            {"driver_number": 7, "position": 11},
        ]
    ]

    result = calculate_points(session, RACE_POINTS)

    assert result[7]["points"] == 0
    assert result[7]["wins"] == 0


def test_calculate_aggregate_points_multiple_sessions():
    sessions = [
        [{"driver_number": 1, "position": 1}],   # 25 pkt, 1 win
        [{"driver_number": 1, "position": 2}],   # 18 pkt
        [{"driver_number": 1, "position": 3}],   # 15 pkt
    ]

    result = calculate_points(sessions, RACE_POINTS)

    assert result[1]["points"] == 25 + 18 + 15
    assert result[1]["wins"] == 1

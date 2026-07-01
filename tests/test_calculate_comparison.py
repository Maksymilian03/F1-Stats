from schemas import DriverStandingInfo
from services import calculate_comparison


def test_calculate_comparison_result_driver1_wins():
    # Arrange
    driver1 = DriverStandingInfo(
        position=1,
        full_name="Driver One",
        driver_number=44,
        team="Team A",
        points=100,
        wins=5
    )
    driver2 = DriverStandingInfo(
        position=2,
        full_name="Driver Two",
        driver_number=33,
        team="Team B",
        points=80,
        wins=3
    )

    # Act
    comparison = calculate_comparison(driver1, driver2)

    # Assert
    assert comparison.points_difference == 20
    assert comparison.wins_difference == 2
    assert comparison.position_difference == 1
    assert comparison.leader == driver1


def test_calculate_comparison_result_driver2_wins():
    # Arrange
    driver1 = DriverStandingInfo(
        position=2,
        full_name="Driver One",
        driver_number=44,
        team="Team A",
        points=100,
        wins=5
    )
    driver2 = DriverStandingInfo(
        position=1,
        full_name="Driver Two",
        driver_number=33,
        team="Team B",
        points=120,
        wins=7
    )

    # Act
    comparison = calculate_comparison(driver1, driver2)

    # Assert
    assert comparison.points_difference == 20
    assert comparison.wins_difference == 2
    assert comparison.position_difference == 1
    assert comparison.leader == driver2


def test_calculate_comparison_draw():
    # Arrange
    driver1 = DriverStandingInfo(
        position=1,
        full_name="Driver One",
        driver_number=44,
        team="Team A",
        points=100,
        wins=5
    )
    driver2 = DriverStandingInfo(
        position=2,
        full_name="Driver Two",
        driver_number=33,
        team="Team B",
        points=100,
        wins=5
    )

    # Act
    comparison = calculate_comparison(driver1, driver2)

    # Assert
    assert comparison.points_difference == 0
    assert comparison.wins_difference == 0

    assert comparison.leader == "draw"


def test_calculate_comparison_result_driver1_wins_by_more_race_wins():
    # Arrange
    driver1 = DriverStandingInfo(
        position=1,
        full_name="Driver One",
        driver_number=44,
        team="Team A",
        points=100,
        wins=6
    )
    driver2 = DriverStandingInfo(
        position=1,
        full_name="Driver Two",
        driver_number=33,
        team="Team B",
        points=100,
        wins=5
    )

    # Act
    comparison = calculate_comparison(driver1, driver2)

    # Assert
    assert comparison.points_difference == 0
    assert comparison.wins_difference == 1
    assert comparison.position_difference == 0
    assert comparison.leader == driver1

from unittest.mock import AsyncMock, patch

import pytest

from schemas import CompareResponse, DriverStandingInfo
from services import get_comparison_drivers


@pytest.mark.asyncio
@patch('services.load_comparison_data_from_db', new_callable=AsyncMock)
@patch('services.get_driver_standings', new_callable=AsyncMock)
async def test_get_comparison_drivers(mock_get_driver_standings, mock_load_comparison_data_from_db, mock_session):
    # Arrange

    mock_load_comparison_data_from_db.return_value = (
        DriverStandingInfo(position=1, full_name="Lewis Hamilton", driver_number=44, team="Mercedes", points=100, wins=5),
        DriverStandingInfo(position=2, full_name="Max Verstappen", driver_number=3, team="Red Bull", points=80, wins=3)
    )

    # Act
    result = await get_comparison_drivers(2024, 44, 3, session=mock_session)

    # Assert
    assert isinstance(result, CompareResponse)
    assert result.driver1.full_name == "Lewis Hamilton"
    assert result.driver2.full_name == "Max Verstappen"
    assert result.comparison.points_difference == 20
    assert result.comparison.wins_difference == 2
    mock_get_driver_standings.assert_awaited_once_with(2024, mock_session)
    mock_load_comparison_data_from_db.assert_awaited_once_with(2024, 44, 3, mock_session)

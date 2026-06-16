from unittest.mock import AsyncMock, patch


@patch("services.get_races_and_sprints", new_callable=AsyncMock)
async def test_get_driver_standings_returns_empty_list_when_no_races(
    mock_get_races_and_sprints, client
):
    # Arrange
    mock_get_races_and_sprints.return_value = ([], [])

    # Act
    response = await client.get("/standings/2023/")

    # Assert
    assert response.status_code == 200
    assert response.json() == []
    mock_get_races_and_sprints.assert_called_once_with(2023)
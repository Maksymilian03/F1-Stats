from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
from fastapi import HTTPException


@pytest.mark.asyncio
@patch('services.httpx.AsyncClient')
async def test_fetch_drivers_returns_dict_of_drivers(mock_async_client):
    # ARRANGE: zbuduj strukturę mocków

    # Fake odpowiedź z OpenF1 (lista kierowców)
    fake_drivers_data = [
        {"driver_number": 1, "full_name": "Max Verstappen", "team_name": "Red Bull"},
        {"driver_number": 44, "full_name": "Lewis Hamilton", "team_name": "Mercedes"},
    ]

    # response.json() zwraca dane
    mock_response = MagicMock()
    mock_response.json.return_value = fake_drivers_data
    mock_response.raise_for_status = MagicMock()  # nic nie robi (nie rzuca)

    # client.get(url) zwraca response (async!)
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)

    # async with httpx.AsyncClient() as client → daje nam mock_client
    mock_async_client.return_value.__aenter__.return_value = mock_client

    # ACT
    from services import fetch_drivers
    result = await fetch_drivers(session_key='latest')

    # ASSERT
    assert 1 in result
    assert result[1]['full_name'] == "Max Verstappen"
    assert 44 in result
    assert result[44]['team_name'] == "Mercedes"


@pytest.mark.asyncio
@patch('services.httpx.AsyncClient')
async def test_fetch_drivers_raises_404_when_no_data(mock_async_client):
    # ARRANGE: zbuduj strukturę mocków

    #Fake odpowiedź z OpenF1 (brak danych)
    fake_drivers_data = {"detail": "No results found"}

    # response.json() zwraca dane
    mock_response = MagicMock()
    mock_response.json.return_value = fake_drivers_data
    mock_response.raise_for_status = MagicMock()

    # client.get(url) zwraca response (async!)
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)

    # async with httpx.AsyncClient() as client → daje nam mock_client
    mock_async_client.return_value.__aenter__.return_value = mock_client

    # ACT & ASSERT
    from services import fetch_drivers
    with pytest.raises(HTTPException) as exc_info:
        await fetch_drivers(session_key='latest')

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Nie znaleziono kierowców"


@pytest.mark.asyncio
@patch('services.httpx.AsyncClient')
async def test_fetch_drivers_raises_502_when_openf1_returns_5xx(mock_async_client):
    # ARRANGE: zbuduj strukturę mocków

    #Fake odpowiedź z OpenF1 (błąd serwera)
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "500 Server error", request=MagicMock(), response=MagicMock(status_code=500)
    )

    # client.get(url) zwraca response (async!)
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)

    # async with httpx.AsyncClient() as client → daje nam mock_client
    mock_async_client.return_value.__aenter__.return_value = mock_client

    # ACT & ASSERT
    from services import fetch_drivers
    with pytest.raises(HTTPException) as exc_info:
        await fetch_drivers(session_key='latest')

    assert exc_info.value.status_code == 502
    assert 'OpenF1 Api error' in exc_info.value.detail


@pytest.mark.asyncio
@patch('services.httpx.AsyncClient')
async def test_fetch_drivers_raises_503_when_no_connection(mock_async_client):
    # ARRANGE: zbuduj strukturę mocków

    #Fake odpowiedź z OpenF1 (błąd połączenia)
    mock_client = AsyncMock()
    mock_client.get.side_effect = httpx.ConnectError("Connection error")

    # async with httpx.AsyncClient() as client → daje nam mock_client
    mock_async_client.return_value.__aenter__.return_value = mock_client

    # ACT & ASSERT
    from services import fetch_drivers
    with pytest.raises(HTTPException) as exc_info:
        await fetch_drivers(session_key='latest')

    assert exc_info.value.status_code == 503

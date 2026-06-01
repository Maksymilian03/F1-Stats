from unittest.mock import patch

import pytest


@pytest.mark.asyncio
@patch('services._fetch_openf1')
async def test_fetch_session_results_returns_dict_of_results(mock_fetch_openf1):

    fake_session_results = [
        {"position": 1, "driver_number": 44, "number_of_laps": 44, "points": 25,
            "dnf": False, "dns": False, "dsq": False,
            "duration": 4797.566, "gap_to_leader": 0, "meeting_key": 1242, "session_key": 9574},
        ]

    mock_fetch_openf1.return_value = fake_session_results
    session_key = 9574
    from services import fetch_session_results
    result = await fetch_session_results(session_key=session_key)

    assert str(session_key) in mock_fetch_openf1.call_args.args[0]
    assert result == fake_session_results





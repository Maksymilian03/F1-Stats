from unittest.mock import patch
import pytest


@pytest.mark.asyncio
@patch('services._fetch_openf1')
async def test_fetch_race_and_sprint_keys_returns_list_of_session_keys(mock_fetch_openf1):

    fake_race_sessions = [
        {"session_key": 9575, "session_name": "Race", "meeting_key": 1242},
        {"session_key": 9573, "session_name": "Race", "meeting_key": 1243},
    ]
    fake_sprint_sessions = [
        {"session_key": 9574, "session_name": "Sprint", "meeting_key": 1242},
        {"session_key": 9572, "session_name": "Sprint", "meeting_key": 1243},
    ]
    year = 2023
    mock_fetch_openf1.side_effect = [fake_race_sessions, fake_sprint_sessions]


    from services import get_races_and_sprints
    race_keys, sprint_keys= await get_races_and_sprints(year)

    assert race_keys == [9575, 9573]
    assert sprint_keys == [9574, 9572]

    assert str(year) in mock_fetch_openf1.call_args_list[0].args[0]
    assert 'session_name=Race' in mock_fetch_openf1.call_args_list[0].args[0]

    assert str(year) in mock_fetch_openf1.call_args_list[1].args[0]
    assert 'session_name=Sprint' in mock_fetch_openf1.call_args_list[1].args[0]


    
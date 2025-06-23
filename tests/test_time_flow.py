import pytest
from src.flows.time_flow import TimeService

@pytest.fixture
def time_service():
    return TimeService()

def test_get_time_returns_string(time_service):
    result = time_service.get_time()
    assert isinstance(result, str)
    assert "The current time is" in result

def test_get_date_returns_string(time_service):
    result = time_service.get_date()
    assert isinstance(result, str)
    assert "Today's date is" in result

def test_get_week_info_returns_string(time_service):
    result = time_service.get_week_info()
    assert isinstance(result, str)
    assert "week" in result

@pytest.mark.parametrize("tokens,expected", [
    (["week"], "week"),
    (["date"], "date"),
    (["time"], "time"),
    (["unknown"], "The current time is"),
])
def test_get_time_info_variants(time_service, tokens, expected):
    result = time_service.get_time_info(tokens)
    assert expected in result
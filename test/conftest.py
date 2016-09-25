import time
import pytest

@pytest.fixture(autouse=True)
def set_timezone(monkeypatch):
    monkeypatch.setenv('TZ', 'EST5EDT,M3.2.0/M11.1.0')
    time.tzset()

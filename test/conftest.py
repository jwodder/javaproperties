import time
import pytest

@pytest.fixture
def fixed_timestamp(mocker):
    mocker.patch('time.localtime', return_value=time.localtime(1478550580))
    yield 'Mon Nov 07 15:29:40 EST 2016'
    time.localtime.assert_called_once_with(None)

from __future__ import annotations
from collections.abc import Iterator
import time
import pytest
from pytest_mock import MockerFixture


@pytest.fixture
def fixed_timestamp(mocker: MockerFixture) -> Iterator[str]:
    m = mocker.patch("time.localtime", return_value=time.localtime(1478550580))
    yield "Mon Nov 07 15:29:40 EST 2016"
    m.assert_called_once_with(None)

import pytest

from flask.helpers import get_root_path


@pytest.fixture()
def tests_root():
    return get_root_path('tests')



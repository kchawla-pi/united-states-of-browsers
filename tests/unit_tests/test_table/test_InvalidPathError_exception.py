from pathlib import Path

import pytest

from united_states_of_browsers.db_merge import InvalidPathError
from united_states_of_browsers.db_merge.table import Table


def test_InvalidPathError_mozilla(create_invalid_dirpath):
    table_obj = Table(table='moz_places',
                      path=create_invalid_dirpath,
                      browser='firefox',
                      filename='places.sqlite',
                      profile='test_profile1',
                      copies_subpath=None,
                      )
    with pytest.raises(InvalidPathError) as excep:
        table_obj.make_records_yielder()


def test_InvalidPathError_chrome(create_invalid_dirpath):
    table_obj = Table(table='urls',
                      path=create_invalid_dirpath,
                      browser='chrome',
                      filename='History',
                      profile='Profile 1 _wrongpath_',
                      copies_subpath=None,
                      )
    with pytest.raises(InvalidPathError) as excep:
        table_obj.make_records_yielder()


def test_InvalidPathError_vivaldi(create_invalid_dirpath):
    table_obj = Table(table='urls',
                      path=create_invalid_dirpath,
                      browser='vivaldi',
                      filename='History',
                      profile='Default',
                      copies_subpath=None,
                      )
    with pytest.raises(InvalidPathError) as excep:
        table_obj.make_records_yielder()


def test_InvalidPathError_opera(create_invalid_dirpath):
    table_obj = Table(table='urls',
                      path=create_invalid_dirpath,
                      browser='opera',
                      filename='History',
                      profile='Opera Stable',
                      copies_subpath=None,
                      )
    with pytest.raises(InvalidPathError) as excep:
        table_obj.make_records_yielder()

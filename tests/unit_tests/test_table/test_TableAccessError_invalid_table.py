import pytest

from united_states_of_browsers.db_merge.table import Table
from united_states_of_browsers.db_merge.custom_exceptions import TableAccessError


def test_TableAccessError_mozilla(create_mozilla_data):
    table_obj = Table(table='invalid_tablename',
                      path=create_mozilla_data,
                      browser='firefox',
                      filename='places.sqlite',
                      profile='test_profile2',
                      copies_subpath=None,
                      )
    with pytest.raises(TableAccessError):
        table_obj.make_records_yielder()


def test_TableAccessError_chrome(create_chromium_data):
    table_obj = Table(table='nonexistent_table',
                      path=create_chromium_data,
                      browser='chrome',
                      filename='History',
                      profile='Profile 1',
                      copies_subpath=None,
                      )
    with pytest.raises(TableAccessError):
        table_obj.make_records_yielder()

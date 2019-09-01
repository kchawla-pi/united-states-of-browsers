import pytest

from pathlib import Path

from united_states_of_browsers.db_merge.table import Table
from united_states_of_browsers.db_merge.custom_exceptions import TableAccessError


def test_TableAccessError_mozilla(create_fake_non_db_file):
    table_obj = Table(table='moz_places',
                      path=create_fake_non_db_file,
                      browser='firefox',
                      filename='places.sqlite',
                      profile='test_profile2',
                      copies_subpath=None,
                      )
    with pytest.raises(TableAccessError):
        table_obj.make_records_yielder()


def test_TableAccessError_chrome(create_fake_non_db_file):
    table_obj = Table(table='nonexistent_table',
                      path=create_fake_non_db_file,
                      browser='chrome',
                      filename='History',
                      profile='Profile 1',
                      copies_subpath=None,
                      )
    with pytest.raises(TableAccessError):
        table_obj.make_records_yielder()


def test_TableAccessError_vivaldi(create_fake_non_db_file):
    table_obj = Table(table='nonexistent_table',
                      path=create_fake_non_db_file,
                      browser='vivaldi',
                      filename='History',
                      profile='Default',
                      copies_subpath=None,
                      )
    with pytest.raises(TableAccessError):
        table_obj.make_records_yielder()


def test_TableAccessError_opera(create_fake_non_db_file):
    table_obj = Table(table='nonexistent_table',
                      path=create_fake_non_db_file,
                      browser='opera',
                      filename='History',
                      profile='Opera Stable',
                      copies_subpath=None,
                      )
    with pytest.raises(TableAccessError):
        table_obj.make_records_yielder()

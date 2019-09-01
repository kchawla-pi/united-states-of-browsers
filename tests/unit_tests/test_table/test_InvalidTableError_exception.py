import pytest

from pathlib import Path

from united_states_of_browsers.db_merge.table import Table
from united_states_of_browsers.db_merge.custom_exceptions import InvalidTableError


def test_InvalidTableError_mozilla(create_fake_non_db_file):
    table_obj = Table(table='moz_places',
                      path=create_fake_non_db_file,
                      browser='firefox',
                      filename='places.sqlite',
                      profile='test_profile2',
                      copies_subpath=None,
                      )
    with pytest.raises(InvalidTableError):
        table_obj.make_records_yielder()


def test_InvalidTableError_chrome(create_fake_non_db_file):
    table_obj = Table(table='nonexistent_table',
                      path=create_fake_non_db_file,
                      browser='chrome',
                      filename='History',
                      profile='Profile 1',
                      copies_subpath=None,
                      )
    with pytest.raises(InvalidTableError):
        table_obj.make_records_yielder()


def test_InvalidTableError_vivaldi(create_fake_non_db_file):
    table_obj = Table(table='nonexistent_table',
                      path=create_fake_non_db_file,
                      browser='vivaldi',
                      filename='History',
                      profile='Default',
                      copies_subpath=None,
                      )
    with pytest.raises(InvalidTableError):
        table_obj.make_records_yielder()


def test_InvalidTableError_opera(create_fake_non_db_file):
    table_obj = Table(table='nonexistent_table',
                      path=create_fake_non_db_file,
                      browser='opera',
                      filename='History',
                      profile='Opera Stable',
                      copies_subpath=None,
                      )
    with pytest.raises(InvalidTableError):
        table_obj.make_records_yielder()


# TableArgs(table='moz_places',
#              path=Path(
#                     'data/browser_profiles_for_testing/AppData/Roaming/Mozilla/'
#                     'Firefox/Profiles/e0pj4lec.test_profile0/places.sqlite'),
#              browser='firefox',
#              filename='places.sqlite',
#              profile='test_profile0',
#              copies_subpath=None,
#
#              ),

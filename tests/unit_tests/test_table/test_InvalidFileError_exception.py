import pytest
from pathlib import Path

from united_states_of_browsers.db_merge.table import Table
from united_states_of_browsers.db_merge.custom_exceptions import (
    InvalidFileError,
    )


def test_InvalidFileError_mozilla_1(tests_root):
    table_obj = Table(table='moz_places',
                      path=Path(tests_root,
                                'tests/data/browser_profiles_for_testing/AppData/Roaming/Mozilla/'
                                'Firefox/Profiles/udd5sttq.test_profile2/non_db_dummy_file_for_testing.txt'),
                      browser='firefox',
                      filename='non_db_dummy_file_for_testing.txt',
                      profile='test_profile2',
                      copies_subpath=None,
                      )
    with pytest.raises(InvalidFileError):
        table_obj.make_records_yielder()


def test_InvalidFileError_mozilla_2(tests_root):
    table_obj = Table(table='moz_places',
                      path=Path(tests_root,
                                'tests/data/browser_profiles_for_testing/AppData/Roaming/Mozilla/'
                                'Firefox/Profiles/udd5sttq.test_profile2/places_non_existent.sqlite'),
                      browser='firefox',
                      filename='places_non_existent.sqlite',
                      profile='test_profile2',
                      copies_subpath=None,
                      )
    with pytest.raises(InvalidFileError):
        table_obj.make_records_yielder()


def test_InvalidFileError_chrome(tests_root):
    table_obj = Table(table='urls',
                      path=Path(tests_root,
                                'tests/data/browser_profiles_for_testing/AppData/Local/Google/Chrome/User Data/Profile 1/History_false_filename'),
                      browser='chrome',
                      filename='History_false_filename',
                      profile='Profile 1',
                      copies_subpath=None,
                      )
    with pytest.raises(InvalidFileError):
        table_obj.make_records_yielder()


def test_InvalidFileError_vivaldi(tests_root):
    table_obj = Table(table='urls',
                      path=Path(tests_root,
                                'tests/data/browser_profiles_for_testing/AppData/Local/Vivaldi/User Data/Default/History_false_filename'),
                      browser='vivaldi',
                      filename='History',
                      profile='Default',
                      copies_subpath=None,
                      )
    with pytest.raises(InvalidFileError):
        table_obj.make_records_yielder()


def test_InvalidFileError_opera(tests_root):
    table_obj = Table(table='urls',
                      path=Path(tests_root,
                                'tests/data/browser_profiles_for_testing/AppData/Roaming/Opera Software/Opera Stable/History_false_filename'),
                      browser='opera',
                      filename='History',
                      profile='Opera Stable',
                      copies_subpath=None,
                      )
    with pytest.raises(InvalidFileError):
        table_obj.make_records_yielder()

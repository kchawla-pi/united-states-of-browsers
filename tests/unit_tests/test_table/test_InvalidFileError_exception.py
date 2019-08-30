import pytest
from pathlib import Path

from united_states_of_browsers.db_merge.table import Table
from united_states_of_browsers.db_merge.custom_exceptions import (
    InvalidFileError,
    )


def test_InvalidFileError_mozilla_1(create_invalid_filepath):
    table_obj = Table(table='moz_places',
                      path=create_invalid_filepath,
                      browser='firefox',
                      filename='non_db_dummy_file_for_testing.txt',
                      profile='test_profile2',
                      copies_subpath=None,
                      )
    with pytest.raises(InvalidFileError):
        table_obj.make_records_yielder()


def test_InvalidFileError_mozilla_2(create_invalid_filepath):
    table_obj = Table(table='moz_places',
                      path=create_invalid_filepath,
                      browser='firefox',
                      filename='places_non_existent.sqlite',
                      profile='test_profile2',
                      copies_subpath=None,
                      )
    with pytest.raises(InvalidFileError):
        table_obj.make_records_yielder()


def test_InvalidFileError_chrome(create_invalid_filepath):
    table_obj = Table(table='urls',
                      path=create_invalid_filepath,
                      browser='chrome',
                      filename='History_false_filename',
                      profile='Profile 1',
                      copies_subpath=None,
                      )
    with pytest.raises(InvalidFileError):
        table_obj.make_records_yielder()


def test_InvalidFileError_vivaldi(create_invalid_filepath):
    table_obj = Table(table='urls',
                      path=create_invalid_filepath,
                      browser='vivaldi',
                      filename='History',
                      profile='Default',
                      copies_subpath=None,
                      )
    with pytest.raises(InvalidFileError):
        table_obj.make_records_yielder()


def test_InvalidFileError_opera(create_invalid_filepath):
    table_obj = Table(table='urls',
                      path=create_invalid_filepath,
                      browser='opera',
                      filename='History',
                      profile='Opera Stable',
                      copies_subpath=None,
                      )
    with pytest.raises(InvalidFileError):
        table_obj.make_records_yielder()

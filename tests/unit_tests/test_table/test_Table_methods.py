import filecmp
import sqlite3
import tempfile
from pathlib import Path

import pytest

from united_states_of_browsers.db_merge.table import Table


def test_suite_no_exceptions_chromium(create_chromium_data):
    with tempfile.TemporaryDirectory() as tempdir:
        chromium_db_path = create_chromium_data
        table_obj = Table(table='urls',
                          path=chromium_db_path,
                          browser='chrome',
                          filename='History',
                          profile='Profile 1',
                          copies_subpath=tempdir,
                          )
        table_obj.make_records_yielder()
        for entry in table_obj.records_yielder:
            entry


def test_suite_no_exceptions_mozilla(create_mozilla_data):
    mozilla_db_path = create_mozilla_data
    table_obj = Table(table='moz_places',
                      path=mozilla_db_path,
                      browser='firefox',
                      filename='places.sqlite',
                      profile='test_profile0',
                      copies_subpath=None,
                      )
    table_obj.make_records_yielder()
    for entry in table_obj.records_yielder:
        entry


def test_check_if_empty_db_true(create_chromium_data):
    with tempfile.TemporaryDirectory() as tmpdir:
        dbname = 'empty.sqlite'
        dbpath = str(Path(tmpdir, dbname))
        conn = sqlite3.connect(dbpath)
        conn.close()
        empty_ = Table(table='nonexistent_table',
                      path=dbpath,
                      browser=None,
                      filename=dbname,
                      profile=None,
                      )
        empty_._connect()
        assert empty_.check_if_db_empty() == True
        empty_._connection.close()


def test_check_if_empty_db_false(create_chromium_data):
    not_empty_table = Table(table='urls',
                            path=create_chromium_data,
                            browser=None,
                            filename='anything',
                            profile=None,
                            )
    not_empty_table._connect()
    assert not_empty_table.check_if_db_empty() == False
    
    
def test_create_db_copy(create_mozilla_data):
    with tempfile.TemporaryDirectory() as tempdir:
        table = Table(table='moz_places',
                      path=create_mozilla_data,
                      browser='mozilla',
                      filename='anything',
                      profile='test',
                      copies_subpath=tempdir,
                      )
        filename = Path(create_mozilla_data).name
        expected_dst = Path(table.copies_subpath, 'AppData', 'Profile Copies',
                            table.browser,
                            table.profile, filename).expanduser()
        table._create_db_copy()
        assert table.path == expected_dst
        assert filecmp.cmp(expected_dst, table.path)


def test_create_db_copy_invalid_parameter_names(create_mozilla_data):
    table = Table(table='moz_places',
                  path=create_mozilla_data,
                  browser=None,
                  filename=None,
                  profile=None,
                  copies_subpath='.',
                  )
    with pytest.raises(TypeError):
        table._create_db_copy()
        
        
def test_create_db_copy_invalid_FileNotFoundError(create_invalid_filepath):
    with tempfile.TemporaryDirectory() as tempdir:
        table = Table(table='some_table',
                      path=create_invalid_filepath,
                      browser='mozilla',
                      filename='anything',
                      profile='test',
                      copies_subpath=tempdir,
                      )
        excep = table._create_db_copy()
        assert isinstance(excep, FileNotFoundError)
        
        
def test_connect_FileNotFoundError(tests_root):
    invalid_path = str(Path(tests_root, 'invalid0', 'invalid1', 'invalid2'))
    table = Table(table='some_table',
                  path=invalid_path,
                  browser='mozilla',
                  filename='anything',
                  profile='test',
                  )
    excep = table._connect()
    assert isinstance(excep, FileNotFoundError)


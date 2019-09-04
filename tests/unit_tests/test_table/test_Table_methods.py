import filecmp
import sqlite3
import tempfile
from collections import namedtuple
from pathlib import Path

import pytest

from united_states_of_browsers.db_merge.custom_exceptions import \
    TableAccessError
from united_states_of_browsers.db_merge.table import Table


def test_table_no_exceptions_chromium_db_copy(create_chromium_data):
    with tempfile.TemporaryDirectory() as tempdir:
        expected_record = {'id': 88,
                           'url': 'https://www.google.com/search?q=chrome+linux+profile+data&oq=chrome+linux+profile+data&aqs=chrome..69i57j33l4.3443j0j7&sourceid=chrome&ie=UTF-8',
                           'title': 'chrome linux profile data - Google Search',
                           'visit_count': 1, 'typed_count': 0,
                           'last_visit_time': 13204503690648295, 'hidden': 0,
                           'last_visit_readable': '2388-06-07 16:41:30',
                           }
        chromium_db_path = create_chromium_data
        table_obj = Table(table='urls',
                          path=chromium_db_path,
                          browser='chrome',
                          filename='History',
                          profile='Profile 1',
                          copies_subpath=tempdir,
                          )
        table_obj.make_records_yielder()
        records = list(table_obj.records_yielder)
        assert len(records) == 1
        assert records[0] ==expected_record
        del table_obj


def test_table_no_exceptions_mozilla_timestamp_field(create_mozilla_data):
    mozilla_db_path = create_mozilla_data
    table_obj = Table(table='moz_places',
                      path=mozilla_db_path,
                      browser='firefox',
                      filename='places.sqlite',
                      profile='test_profile0',
                      copies_subpath=None,
                      )
    table_obj.make_records_yielder()
    records = list(table_obj.records_yielder)
    assert len(records) == 3
    assert [record['id'] for record in records] == [13, 1, 1]
    assert any([key.endswith('_readable') for key in records[0].keys()])


def test_table_mozilla_table_no_timestamp_field(create_mozilla_data):
    mozilla_db_path = Path(create_mozilla_data)
    table_obj = Table(table='moz_origins',
                      path=mozilla_db_path,
                      browser='firefox',
                      filename='places.sqlite',
                      profile='test_profile1',
                      copies_subpath=None,
                      )
    table_obj.make_records_yielder()
    records = list(table_obj.records_yielder)
    assert len(records) == 1
    assert records[0]['id'] == 1
    assert not all([key.endswith('_readable') for key in records[0].keys()])
    
    
@pytest.mark.parametrize('field_names', [field_names for field_names in (['id', 'last_visit_date'], ['id', 'last_visit_time'])])
def test_check_timestamp_field(field_names):
    expected_output = {field_names[1]: 'last_visit_readable'}
    cursor_desc_mimic = [[field, None, None, None] for field in field_names]
    CursorDescription = namedtuple('CursorDescription', 'description')
    cursor_mimic = CursorDescription(description=cursor_desc_mimic)
    actual_output= Table._check_timestamp_field(Table, cursor=cursor_mimic)
    assert expected_output == actual_output


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
    
    
def test_make_records_yielder_invalid_FileNotFoundError(create_invalid_filepath):
    with tempfile.TemporaryDirectory() as tempdir:
        table = Table(table='some_table',
                      path=create_invalid_filepath,
                      browser='mozilla',
                      filename='anything',
                      profile='test',
                      copies_subpath=tempdir,
                      )
        records_yielder, excep = table.make_records_yielder()
        assert records_yielder is None
        assert isinstance(excep, FileNotFoundError)


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


def test_invalid_filepath_error_mozilla_1(create_invalid_filepath):
    table_obj = Table(table='moz_places',
                      path=create_invalid_filepath,
                      browser='firefox',
                      filename='non_db_dummy_file_for_testing.txt',
                      profile='test_profile2',
                      copies_subpath=None,
                      )
    with pytest.raises(sqlite3.OperationalError) as excep:
        table_obj.make_records_yielder()
        assert str(excep) == 'unable to open database file'


def test_TableAccessError_invalid_table(create_mozilla_data):
    table_obj = Table(table='invalid_tablename',
                      path=create_mozilla_data,
                      browser='firefox',
                      filename='places.sqlite',
                      profile='test_profile2',
                      copies_subpath=None,
                      )
    with pytest.raises(TableAccessError):
        table_obj.make_records_yielder()


def test_TableAccessError_nondb_mozilla(create_fake_non_db_file):
    table_obj = Table(table='moz_places',
                      path=create_fake_non_db_file,
                      browser='firefox',
                      filename='places.sqlite',
                      profile='test_profile2',
                      copies_subpath=None,
                      )
    with pytest.raises(TableAccessError):
        table_obj.make_records_yielder()


def test_TableAccessError_nondb_chrome(create_fake_non_db_file):
    table_obj = Table(table='nonexistent_table',
                      path=create_fake_non_db_file,
                      browser='chrome',
                      filename='History',
                      profile='Profile 1',
                      copies_subpath=None,
                      )
    with pytest.raises(TableAccessError):
        table_obj.make_records_yielder()

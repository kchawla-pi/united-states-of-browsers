import sqlite3
import tempfile
from pathlib import Path

from united_states_of_browsers.db_merge.table import Table


def test_suite_no_exceptions_chromium(create_chromium_data):
    chromium_db_path = create_chromium_data
    table_obj = Table(table='urls',
                      path=chromium_db_path,
                      browser='chrome',
                      filename='History',
                      profile='Profile 1',
                      copies_subpath=None,
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


def test_check_if_emoty_db(create_chromium_data):
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
        
    not_empty_table = Table(table='urls',
                            path=create_chromium_data,
                            browser=None,
                            filename='anything',
                            profile=None,
                            )
    not_empty_table._connect()
    assert not_empty_table.check_if_db_empty() == False

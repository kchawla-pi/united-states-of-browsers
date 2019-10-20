import os
import sqlite3
import tempfile
import warnings
from pathlib import Path

import pytest

from united_states_of_browsers.db_merge import browser_data
from united_states_of_browsers.db_merge.db_merge import (
    BrowserData,
    DatabaseMergeOrchestrator,
    orchestrate_db_merge,
    write_db_path_to_file,
    write_records,
    rename_existing_db,
    make_records_yielders,
    find_installed_browsers
    )
from united_states_of_browsers.db_merge.db_search import check_fts5_installed
from united_states_of_browsers.db_merge.helpers import get_warnings_text


def _make_data_for_tests(tests_root):
    firefox_info = BrowserData(os=os.name,
                               browser='firefox',
                               path=Path(tests_root, 'firefox_databases'),
                               profiles=None,
                               file_tables={'places.sqlite': ['moz_places']},
                               table_fields={'moz_places': ['id', 'url', 'title',
                                                            'visit_count',
                                                            'last_visit_date',
                                                            'last_visit_readable']
                                             }
                               )

    chrome_info = BrowserData(os=os.name,
                              browser='chrome',
                              path=Path(tests_root, 'chrome_databases'),
                              profiles=None,
                              file_tables={'History': ['urls']},
                              table_fields={'urls': ['id', 'url', 'title',
                                                     'visit_count',
                                                     'last_visit_time',
                                                     'last_visit_readable']
                                            }
                              )
    opera_info = BrowserData(os=os.name,
                              browser='opera',
                              path=Path(tests_root, 'opera_databases'),
                              profiles=None,
                              file_tables={'History': ['urls']},
                              table_fields={'urls': ['id', 'url', 'title',
                                                     'visit_count',
                                                     'last_visit_time',
                                                     'last_visit_readable']
                                            }
                              )
    browser_info = [firefox_info, chrome_info, opera_info]
    return browser_info


def test_find_installed_browsers(tests_root):
    browser_info = _make_data_for_tests(tests_root)
    combined_db = DatabaseMergeOrchestrator(app_path=tests_root,
                                            db_name='test_combi_db',
                                            browser_info=browser_info,
                                            )
    assert combined_db.installed_browsers_data is None
    find_installed_browsers(combined_db)
    assert len(combined_db.installed_browsers_data) == 2
    assert combined_db.installed_browsers_data[0].path == Path(
            tests_root,
            'firefox_databases',
            )
    assert combined_db.installed_browsers_data[1].path == Path(
            tests_root,
            'chrome_databases',
            )


def test_make_records_yielder(tests_root):
    browser_info = _make_data_for_tests(tests_root)
    combined_db = DatabaseMergeOrchestrator(app_path=tests_root,
                                            db_name='test_combi_db',
                                            browser_info=browser_info,
                                            )
    find_installed_browsers(combined_db)
    make_records_yielders(combined_db)
    combi_records = [browser_records
                      for browser_records_yielder in combined_db.browser_yielder
                      for browser_records in browser_records_yielder
                      ]
    browser_names = []
    profile_names = []
    urls = {'firefox': list(),
            'chrome': list(),
            }
    for record in combi_records:
        current_browser = record['browser']
        current_profile = record['profile']
        current_url = record['url']

        browser_names.append(current_browser)
        profile_names.append(current_profile)
        urls[current_browser].append(current_url)

    unique_browsers = set(browser_names)
    unique_profiles = set(profile_names)

    assert unique_browsers == {'firefox', 'chrome'}
    assert unique_profiles == {'t87e6f86.test_profile1',
                               'z786c76dv78.test_profile2',
                               'Profile 1',
                               'Profile 2',
                               }
    browser_counts = {browser_name_: browser_names.count(browser_name_)
                      for browser_name_ in unique_browsers
                      }
    assert browser_counts['firefox'] == 18 + 20
    assert browser_counts['chrome'] == 4 + 9

    profile_counts = {profile_name_: profile_names.count(profile_name_)
                      for profile_name_ in unique_profiles
                      }
    assert profile_counts['t87e6f86.test_profile1'] == 18
    assert profile_counts['z786c76dv78.test_profile2'] == 20
    assert profile_counts['Profile 1'] == 4
    assert profile_counts['Profile 2'] == 9

    unique_urls = {'firefox': set(urls['firefox']),
                   'chrome': set(urls['chrome']),
                   }
    assert len(unique_urls['firefox']) == 18 + 20 - 13
    assert len(unique_urls['chrome']) == 4 + 9


def test_rename_existing_db():
    with tempfile.TemporaryDirectory() as tmp_dir:
        combined_db = DatabaseMergeOrchestrator(app_path=tmp_dir,
                                                # case when path == [dirnames]
                                                db_name='test_combi_db',
                                                browser_info=None,
                                                )
        renamed_db_path = Path(tmp_dir, '_previous_test_combi_db')
        combined_db.output_db.write_text('junk')
        assert combined_db.output_db.exists()
        assert not renamed_db_path.exists()
        rename_existing_db(combined_db)
        assert not combined_db.output_db.exists()
        assert renamed_db_path.exists()
        # case when previous db file exists
        rename_existing_db(combined_db)


def test_rename_existing_db_delete_existing_backup():
    # case when previous db file backup exists
    with tempfile.TemporaryDirectory() as tmp_dir:
        combined_db = DatabaseMergeOrchestrator(app_path=[tmp_dir, ''],
                                                # case when path == [dirnames]
                                                db_name='test_combi_db',
                                                browser_info=None,
                                                )
        renamed_db_path = Path(tmp_dir, '_previous_test_combi_db')
        combined_db.output_db.write_text('junk')
        renamed_db_path.write_text('1')
        assert combined_db.output_db.exists()
        assert renamed_db_path.exists()
        assert os.path.getsize(renamed_db_path) == 1
        assert os.path.getsize(combined_db.output_db) == 4

        rename_existing_db(combined_db)
        assert not combined_db.output_db.exists()
        assert renamed_db_path.exists()
        assert os.path.getsize(renamed_db_path) == 4


def test_write_records():
    mock_browsers_records = [
        [{'field1': 'b1p1r1v1', 'field2': 'b1p1r1v2'},
        {'field1': 'b1p2r2v1', 'field2': 'b1p2r2v2'},
        ],
        [{'field1': 'b2p1r1v1', 'field2': 'b2p1r1v2'},
        {'field1': 'b2p2r2v1', 'field2': 'b2p2r2v2'},
        ]]
    browser_yielder = (browser for browser in mock_browsers_records)
    mock_records_generator = (record for record in browser_yielder)
    expected_records = [record
                        for browser in mock_browsers_records
                        for record in browser
                        ]
    def _test_write_record_(tmp_dir):
        """ Nested function to run the test code,
        ensuring all open handles are closed
        so clean up on Windows does not glitch
        due to PermissionError with open file handles.
        """
        combined_db = DatabaseMergeOrchestrator(app_path=tmp_dir,
                                                db_name='test_combi_db',
                                                browser_info=None,
                                                )
        combined_db.browser_yielder = mock_records_generator
        tablename = 'junk_table'
        write_records(combined_db,
                      tablename=tablename,
                      primary_key_name='rec_num',
                      fieldnames=['field1', 'field2'],
                      )

        with sqlite3.connect(str(combined_db.output_db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            query_results = cur.execute(f'SELECT * FROM {tablename}')
            queried_records = query_results.fetchall()
        for num, record in enumerate(expected_records, start=1):
            record.update({'rec_num': num})
        actual_records = [dict(record) for record in queried_records]
        assert actual_records == expected_records

    with tempfile.TemporaryDirectory() as tmp_dir:
        _test_write_record_(tmp_dir)


def test_write_records_improper_table_name():
    with tempfile.TemporaryDirectory() as tmp_dir:
        combined_db = DatabaseMergeOrchestrator(app_path=tmp_dir,
                                                db_name='test_combi_db',
                                                browser_info=None,
                                                )
        combined_db.browser_yielder = [{},{}]
        tablename = 'junk _table'
        with pytest.raises(ValueError) as excep:
            write_records(combined_db,
                          tablename=tablename,
                          primary_key_name='rec_num',
                          fieldnames=['field1', 'field2'],
                          )
        assert str(excep.value) == ("Table name cannot have spaces. "
                                    "You provided 'junk _table'")


def test_write_db_path_to_file():
    test_db_name = 'test_combi_db'
    with tempfile.TemporaryDirectory() as tmp_dir:
        combined_db = DatabaseMergeOrchestrator(app_path=tmp_dir,
                                                db_name= test_db_name,
                                                browser_info=None,
                                                )
        write_db_path_to_file(combined_db, output_dir=tmp_dir)
        expected_output_path = Path(tmp_dir, 'AppData', 'merged_db_path.txt')
        assert expected_output_path.exists()
        actual_text = expected_output_path.read_text()
        assert actual_text.endswith(test_db_name)


def _core_code_for_testing_db_merge(tmp_dir, browser_info):
    """ Nested function to run the test code,
    ensuring all open handles are closed
    so clean up on Windows does not glitch
    due to PermissionError with open file handles.
    """
    combined_db = DatabaseMergeOrchestrator(app_path=tmp_dir,
                                            db_name='test_combi_db',
                                            browser_info=browser_info,
                                            )
    orchestrate_db_merge(combined_db)
    with sqlite3.connect(str(combined_db.output_db)) as conn:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        res = cur.fetchall()
        tables = [table_tuple[0] for table_tuple in res]

        return tables


# fts5 installation needed.
@pytest.mark.skipif(not check_fts5_installed(),
                    reason='FTS5 unavailable; '
                           'required for search table in test.')
def test_db_merge_with_fts5(tests_root):
    browser_info = _make_data_for_tests(tests_root)
    with tempfile.TemporaryDirectory() as tmp_dir:
        tables = _core_code_for_testing_db_merge(tmp_dir, browser_info)
        assert 'search_table' in tables
        assert 'history' in tables


@pytest.mark.skipif(check_fts5_installed(),
                    reason='FTS5 avaliable, test inappropriate.')
def test_db_merge_without_fts5(tests_root):
    browser_info = _make_data_for_tests(tests_root)
    expected_warning = UserWarning(
            'FTS5 extension for SQLIte not available/enabled. '
            'Search functionality unavailable.'
            )
    with tempfile.TemporaryDirectory() as tmp_dir:
        with warnings.catch_warnings(record=True) as raised_warnings:
            tables = _core_code_for_testing_db_merge(tmp_dir, browser_info)
            warnings_contents = get_warnings_text(raised_warnings)
        msg = str(expected_warning)
        assert msg in warnings_contents
        assert repr(warnings_contents[msg]) == repr(UserWarning)


def test_prep_browser_info():
    all_browsers_info = browser_data.prep_browsers_info()
    browser_particulars = {'os': [], 'browsers': []}
    for browser_info in all_browsers_info:
        browser_particulars['os'].append(browser_info.os)
        browser_particulars['browsers'].append(browser_info.browser)
    browser_particulars['os'].sort()
    browser_particulars['browsers'].sort()
    if os.name == 'nt':
        supported_browsers = ['firefox', 'chrome', 'opera', 'vivaldi']
    elif os.name == 'posix':
        supported_browsers = ['firefox', 'chrome']
    supported_browsers.sort()
    assert browser_particulars['browsers'] == supported_browsers
    assert set(browser_particulars['os']) == {os.name}


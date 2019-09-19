from pathlib import Path
from pprint import pprint

import pytest

from united_states_of_browsers.db_merge.browser import (
    make_browser_records_yielder, make_browser_paths
    )
from united_states_of_browsers.db_merge.helpers import (
    check_records_unique_with_field)
from united_states_of_browsers.db_merge.table import Table



def test_browser_access_single_profile_file_table_with_timestamp(tests_root):
    profile_rootpath = Path(tests_root, 'firefox_databases')
    browser_name = 'firefox'
    table_name = 'moz_places'
    profile_name = 'test_profile1'
    file_name = 'places.sqlite'
    moz_places_records_yielder = make_browser_records_yielder(
        browser=browser_name,
        profile_root=profile_rootpath,
        filename=file_name,
        tablename=table_name,
        profiles=[profile_name],
        )
    print(list(moz_places_records_yielder))
    
    
def test_browser_missing_proflie(tests_root):
    profile_rootpath = Path(tests_root, 'firefox_databases')
    browser_name = 'firefox'
    table_name = 'moz_places'
    profile_name = ['test_profile1_JUNK']
    file_name = 'places.sqlite'
    actual_browser_paths = make_browser_paths(browser='firefox',
                                              profile_root=profile_rootpath,
                                              profiles=profile_name,
                                              )
    moz_places_records_yielder = make_browser_records_yielder(
        browser=browser_name,
        profile_root=profile_rootpath,
        filename=file_name,
        tablename=table_name,
        profiles=profile_name,
        )
    yielded_records = list(moz_places_records_yielder)
    assert actual_browser_paths == {}
    assert yielded_records == []


def test_browser_two_proflies_one_missing(tests_root):
    profile_rootpath = Path(tests_root, 'firefox_databases')
    browser_name = 'firefox'
    table_name = 'moz_places'
    profile_names = ['test_profile1_JUNK', 'test_profile2']
    file_name = 'places.sqlite'
    expected_browser_paths = {
        'test_profile2': Path(profile_rootpath, 'z786c76dv78.test_profile2')
        }
    actual_browser_paths = make_browser_paths(browser='firefox',
                                              profile_root=profile_rootpath,
                                              profiles=profile_names,
                                              )
    moz_places_records_yielder = make_browser_records_yielder(
        browser=browser_name,
        profile_root=profile_rootpath,
        filename=file_name,
        tablename=table_name,
        profiles=profile_names,
        )
    actual_records = list(moz_places_records_yielder)
    pprint(actual_records)
    assert expected_browser_paths == actual_browser_paths
    assert len(actual_records) == 20
    assert [record['id'] for record in actual_records] == list(range(1, 21))
    assert actual_records[0]['url'] == 'http://www.linuxmint.com/start/tessa'


def test_browser_missing_path_1(tests_root):
    profile_rootpath = Path(tests_root, 'firefox_databases')
    browser_name = 'firefox'
    table_name = 'moz_places'
    profile_name = 'test_profile1_JUNK'
    file_name = 'places.sqlite'
    moz_places_records_yielder = make_browser_records_yielder(
        browser=browser_name,
        profile_root=profile_rootpath,
        filename=file_name,
        tablename=table_name,
        profiles=[profile_name],
        )
    print(list(moz_places_records_yielder))


def test_browser_missing_path_2(tests_root):
    profile_rootpath = Path(tests_root, 'firefox_databases_JUNK')
    browser_name = 'firefox'
    table_name = 'moz_places'
    profile_name = 'test_profile1'
    file_name = 'places.sqlite_JUNK'
    moz_places_records_yielder = make_browser_records_yielder(
        browser=browser_name,
        profile_root=profile_rootpath,
        filename=file_name,
        tablename=table_name,
        profiles=[profile_name],
        )
    with pytest.raises(FileNotFoundError):
        list(moz_places_records_yielder)

if __name__ == '__main__':
    tests_root = '/home/kshitij/workspace/united-states-of-browsers/tests'
    test_browser_two_proflies_one_missing(tests_root)
    # test_browser_access_single_profile_file_table_with_timestamp(tests_root)
    # test_browser_missing_proflie(tests_root)
    # test_browser_missing_path_1(tests_root)
    # test_browser_missing_path_2(tests_root)

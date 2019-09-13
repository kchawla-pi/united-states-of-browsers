from pathlib import Path

from united_states_of_browsers.db_merge.browser import (
    make_browser_records_yielder)
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


def test_browser_missing_path_1(tests_root):
    profile_rootpath = Path(tests_root, 'firefox_databases')
    browser_name = 'firefox'
    table_name = 'moz_places'
    profile_name = 'test_profile1_JUNK'
    file_name = 'places.sqlite_JUNK'
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
    print(list(moz_places_records_yielder))

if __name__ == '__main__':
    tests_root = '/home/kshitij/workspace/united-states-of-browsers/tests'
    test_browser_access_single_profile_file_table_with_timestamp(tests_root)
    test_browser_missing_proflie(tests_root)
    test_browser_missing_path_1(tests_root)
    test_browser_missing_path_2(tests_root)

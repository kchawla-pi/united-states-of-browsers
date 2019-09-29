import sqlite3
from pathlib import Path

from united_states_of_browsers.db_merge.browser import (
    make_browser_records_yielder)
from united_states_of_browsers.db_merge.helpers import (
    check_records_unique_with_field)
from united_states_of_browsers.db_merge.table import Table


def test_browser_chrome_access_single_profile_file_table_with_timestamp(
        tests_root):
    profile_rootpath = Path(tests_root, 'chrome_databases')
    browser_name = 'chrome'
    table_name = 'urls'
    profile_name = 'Profile 1'
    file_name = 'History'
    profile_path = Path(profile_rootpath, 'Profile 1', 'History',)
    urls_records_yielder = make_browser_records_yielder(
            browser=browser_name,
            profile_root=profile_rootpath,
            filename=file_name,
            tablename=table_name,
            profiles=[profile_name],
            )
    browser_profile1_records = [record for record in urls_records_yielder]
    sort_by_id = lambda item: item['id']
    browser_profile1_records.sort(key=sort_by_id)
    
    with sqlite3.connect(str(profile_path)) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute('''SELECT * FROM urls''')
        records = [dict(record) for record in cur]

    browser_profile1_records_ids = [record['id'] for record in
                                    browser_profile1_records]
    profile1_records_ids = [record['id'] for record in records]
    
    assert len(records) ==len(browser_profile1_records)
    assert check_records_unique_with_field(records=records, field='id')
    assert check_records_unique_with_field(records=browser_profile1_records,
                                    field='id')
    assert sorted(profile1_records_ids) == sorted(browser_profile1_records_ids)


def test_browser_access_single_profile_file_table_without_timestamp(tests_root):
    profile_rootpath = Path(tests_root, 'chrome_databases')
    profile_path = Path(profile_rootpath,
                        'Profile 1',
                        'History',
                        )
    browser_name = 'chrome'
    table_name = 'keyword_search_terms'
    profile_name = 'Profile 1'
    file_name = 'History'

    urls_records_yielder = make_browser_records_yielder(
            browser=browser_name,
            profile_root=profile_rootpath,
            filename=file_name,
            tablename=table_name,
            profiles=[profile_name],
            )
    browser_profile1_records = [record for record in
                                urls_records_yielder]
    sort_by_id = lambda item: item['url_id']
    browser_profile1_records.sort(key=sort_by_id)

    profile1_table = Table(table=table_name,
                           path=profile_path,
                           browser=browser_name,
                           filename=file_name,
                           profile=profile_name,
                           )
    profile1_table.make_records_yielder()
    table_profile1_records = list(profile1_table.records_yielder)
    table_profile1_records.sort(key=sort_by_id)
    table_profile1_records_ids = [record['url_id'] for record in
                                  table_profile1_records]
    browser_profile1_records_ids = [record['url_id'] for record in
                                    browser_profile1_records]
    assert table_profile1_records_ids == browser_profile1_records_ids


def test_browser_access_two_profiles_same_file_table(tests_root):
    profile_rootpath = Path(tests_root, 'chrome_databases')
    browser_name = 'chrome'
    table_name = 'urls'
    file_name = 'History'
    
    urls_records_yielder = make_browser_records_yielder(
            browser=browser_name,
            profile_root=profile_rootpath,
            filename=file_name,
            tablename=table_name,
            profiles=['Profile 1', 'Profile 2'],
            )
    profile_1_2_records_using_browser = [record for record in urls_records_yielder]
    sort_by_url = lambda item: item['url']
    profile_1_2_records_using_browser.sort(key=sort_by_url)

    profile1_table = Table(table=table_name,
                            path=Path(profile_rootpath,
                                      'Profile 1',
                                      file_name,
                                      ),
                           browser=browser_name,
                            filename=file_name,
                            profile='Profile 1',
                            )
    profile1_table.make_records_yielder()
    profile1_records = list(profile1_table.records_yielder)

    profile2_table = Table(table=table_name,
                            path=Path(profile_rootpath,
                                      'Profile 2',
                                      'History',
                                      ),
                           browser=browser_name,
                            filename=file_name,
                            profile='Profile 2',
                            )
    profile2_table.make_records_yielder()
    profile2_records = list(profile2_table.records_yielder)

    profile_1_2_records_using_tables = [*profile1_records, *profile2_records]
    profile_1_2_records_using_tables.sort(key=sort_by_url)

    table_records_urls = [record['url'] for record in
                          profile_1_2_records_using_tables]
    browser_records_urls = [record['url'] for record in
                            profile_1_2_records_using_browser]
    assert table_records_urls == browser_records_urls
    

def test_browser_access_all_profiles_same_file_table(tests_root):
    profile_rootpath = Path(tests_root, 'chrome_databases')
    profile_path = Path(profile_rootpath,
                        'Profile 1',
                        'History',
                        )
    browser_name = 'chrome'
    table_name = 'urls'
    file_name = 'History'
    urls_records_yielder = make_browser_records_yielder(
            browser=browser_name,
            profile_root=profile_rootpath,
            filename=file_name,
            tablename=table_name,
            profiles=None,
            )

    profile_1_2_records_using_browser = [record for record in urls_records_yielder]
    sort_by_url = lambda item: item['url']
    profile_1_2_records_using_browser.sort(key=sort_by_url)

    profile1_table = Table(table=table_name,
                            path=Path(profile_rootpath,
                                      'Profile 1',
                                      file_name,
                                      ),
                           browser=browser_name,
                            filename=file_name,
                            profile='Profile 1',
                            )
    profile1_table.make_records_yielder()
    profile1_records = list(profile1_table.records_yielder)

    profile2_table = Table(table=table_name,
                            path=Path(profile_rootpath,
                                      'Profile 2',
                                      'History',
                                      ),
                           browser=browser_name,
                            filename=file_name,
                            profile='Profile 2',
                            )
    profile2_table.make_records_yielder()
    profile2_records = list(profile2_table.records_yielder)

    profile_1_2_records_using_tables = [*profile1_records, *profile2_records]
    profile_1_2_records_using_tables.sort(key=sort_by_url)

    table_records_urls = [record['url'] for record in
                          profile_1_2_records_using_tables]
    browser_records_urls = [record['url'] for record in
                            profile_1_2_records_using_browser]
    assert table_records_urls == browser_records_urls


def test_browser_chrome_access_filtered_fields(
        tests_root):
    profile_rootpath = Path(tests_root, 'chrome_databases')
    browser_name = 'chrome'
    table_name = 'urls'
    profile_name = 'Profile 1'
    file_name = 'History'
    fields = ['id', 'url', 'title',
              'last_visit_time',
              'last_visit_readable',
              ]
    urls_records_yielder = make_browser_records_yielder(
            browser=browser_name,
            profile_root=profile_rootpath,
            filename=file_name,
            tablename=table_name,
            profiles=[profile_name],
            fieldnames=fields,
            )
    records = [record for record in urls_records_yielder]
    records_fieldnames = set(tuple(record_.keys()) for record_ in records)
    records_fieldnames = records_fieldnames.pop()
    additional_fields = ('browser', 'profile', 'file', 'table')
    expected_fieldnames = [*fields, *additional_fields]
    assert not set(records_fieldnames).difference(expected_fieldnames)
    

if __name__ == '__main__':  # pragme: no cover
    tests_root = '/home/kshitij/workspace/united-states-of-browsers/tests'
    test_browser_chrome_access_single_profile_file_table_with_timestamp(
            tests_root)

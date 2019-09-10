from pathlib import Path

from united_states_of_browsers.db_merge import browser
from united_states_of_browsers.db_merge.browser import Browser
from united_states_of_browsers.db_merge.helpers import \
    check_records_unique_with_field
from united_states_of_browsers.db_merge.table import Table


def test_browser_access_single_profile_file_table_with_timestamp(tests_root):
    profile_rootpath = Path(tests_root, 'firefox_databases')
    profile_path = Path(profile_rootpath,
                        't87e6f86.test_profile1',
                        'places.sqlite',
                        )
    browser_name = 'firefox'
    table_name = 'moz_places'
    profile_name = 'test_profile1'
    file_name = 'places.sqlite'
    fields=['id', 'url', 'title',
            'last_visit_date',
            'last_visit_readable',
            ]

    
    
    browser_profile1 = Browser(browser=browser_name,
                      profiles=[profile_name],
                      profile_root=profile_rootpath,
                      )
    moz_places_records_yielder = browser_profile1.make_records_yielder(filename=file_name, tablename=table_name)

    browser_profile1_records = [record for record in moz_places_records_yielder]
    sort_by_id = lambda item: item['url']
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
    table_profile1_records_urls = [record['url'] for record in table_profile1_records]
    browser_profile1_records_urls = [record['url'] for record in browser_profile1_records]
    assert table_profile1_records_urls == browser_profile1_records_urls


def test_browser_access_single_profile_file_table_without_timestamp(tests_root):
    profile_rootpath = Path(tests_root, 'firefox_databases')
    profile_path = Path(profile_rootpath,
                        't87e6f86.test_profile1',
                        'places.sqlite',
                        )
    browser_name = 'firefox'
    table_name = 'moz_origins'
    profile_name = 'test_profile1'
    file_name = 'places.sqlite'
    fields=['id', 'prefix', 'host', 'frecency']

    browser_profile1 = Browser(browser=browser_name,
                               profiles=[profile_name],
                               profile_root=profile_rootpath,
                               )
    moz_places_records_yielder = browser_profile1.make_records_yielder(filename=file_name,
                                          tablename=table_name)
    browser_profile1_records = [record for record in
                                moz_places_records_yielder]
    sort_by_id = lambda item: item['id']
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
    table_profile1_records_ids = [record['id'] for record in
                                  table_profile1_records]
    browser_profile1_records_ids = [record['id'] for record in
                                    browser_profile1_records]
    assert table_profile1_records_ids == browser_profile1_records_ids


def test_browser_access_two_profiles_same_file_table(tests_root):
    profile_rootpath = Path(tests_root, 'firefox_databases')
    browser_two_profiles = Browser(browser='firefox',
                      profiles=['test_profile1', 'test_profile2'],
                      profile_root=profile_rootpath,
                      )
    moz_places_records_yielder = browser_two_profiles.make_records_yielder(filename='places.sqlite', tablename='moz_places', )
    profile_1_2_records_using_browser = [record for record in moz_places_records_yielder]
    sort_by_url = lambda item: item['url']
    profile_1_2_records_using_browser.sort(key=sort_by_url)

    profile1_table = Table(table='moz_places',
                            path=Path(profile_rootpath,
                                      't87e6f86.test_profile1',
                                      'places.sqlite',
                                      ),
                           browser='mozilla',
                            filename='places.sqlite',
                            profile='test_profile1',
                            )
    profile1_table.make_records_yielder()
    profile1_records = list(profile1_table.records_yielder)
    
    profile2_table = Table(table='moz_places',
                            path=Path(profile_rootpath,
                                      'z786c76dv78.test_profile2',
                                      'places.sqlite',
                                      ),
                           browser='mozilla',
                            filename='places.sqlite',
                            profile='test_profile2',
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
    profile_rootpath = Path(tests_root, 'firefox_databases')
    browser_name = 'firefox'
    file_name = 'places.sqlite'
    table_name = 'moz_places'
    fields = ['id', 'url', 'title',
              'last_visit_date',
              'last_visit_readable',
              ]
    browser_two_profiles = Browser(browser=browser_name,
                                   profiles=None,
                                   profile_root=profile_rootpath,
                                   )
    moz_places_records_yielder = browser_two_profiles.make_records_yielder(filename=file_name,
                                               tablename=table_name )
    profile_1_2_records_using_browser = [record for record in
                                         moz_places_records_yielder]
    sort_by_url = lambda item: item['url']
    profile_1_2_records_using_browser.sort(key=sort_by_url)
    
    profile1_table = Table(table=table_name,
                           path=Path(profile_rootpath,
                                     't87e6f86.test_profile1',
                                     'places.sqlite',
                                     ),
                           browser=browser_name,
                           filename=file_name,
                           profile='test_profile1',
                           )
    profile1_table.make_records_yielder()
    profile1_records = list(profile1_table.records_yielder)
    
    profile2_table = Table(table=table_name,
                           path=Path(profile_rootpath,
                                     'z786c76dv78.test_profile2',
                                     'places.sqlite',
                                     ),
                           browser=browser_name,
                           filename=file_name,
                           profile='test_profile2',
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



if __name__ == '__main__':
    tests_root = '/home/kshitij/workspace/united-states-of-browsers/tests'
    profile_rootpath = Path(tests_root, 'firefox_databases')
    browser_two_profiles = Browser(browser='firefox',
                                   profiles=None,
                                   profile_root=profile_rootpath,
                                   )
    # browser_two_profiles.add_tables_for_access(file='places.sqlite',
    #                                            tables=['moz_places'], )
    # moz_places_records_yielder = browser_two_profiles.access_fields(
    #         table='moz_places',
    #         fields=['id', 'url', 'title',
    #                 'last_visit_date',
    #                 'last_visit_readable',
    #                 ]
    #         )
    fields = ['id', 'url', 'title',
              'last_visit_date',
              'last_visit_readable',
              ]
    moz_places_records_yielder = browser_two_profiles.make_records_yielder(filename='places.sqlite',
                                                                           tablename='moz_places',
                                                                           fieldnames=fields,
                                                                           )
    for record in moz_places_records_yielder:
        print(record)

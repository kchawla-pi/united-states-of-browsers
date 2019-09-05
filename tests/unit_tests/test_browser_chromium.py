from pathlib import Path

from united_states_of_browsers.db_merge.browser import Browser
from united_states_of_browsers.db_merge.helpers import \
    check_records_unique_with_field
from united_states_of_browsers.db_merge.table import Table


def test_browser_access_single_profile_file_table_with_timestamp(tests_root):
    profile_rootpath = Path(tests_root, 'chrome_databases')
    profile_path = Path(profile_rootpath,
                        'Profile 1',
                        'History',
                        )
    browser_name = 'chrome'
    table_name = 'urls'
    profile_name = 'History'
    file_name = 'History'
    
    browser_profile1 = Browser(browser=browser_name,
                      profiles=[profile_name],
                      profile_root=profile_rootpath,
                      )
    browser_profile1.add_tables_for_access(file=file_name, tables=[table_name], )
    urls_records_yielder = browser_profile1.access_fields(
            table='urls',
            fields=['id', 'url', 'title',
                    'last_visit_time',
                    'last_visit_readable',
                    ]
            )
    browser_profile1_records = [record for record in urls_records_yielder]
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
    table_profile1_records_ids = [record['id'] for record in table_profile1_records]
    browser_profile1_records_ids = [record['id'] for record in browser_profile1_records]
    assert table_profile1_records_ids == browser_profile1_records_ids
    
    
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
    
    browser_profile1 = Browser(browser=browser_name,
                               profiles=[profile_name],
                               profile_root=profile_rootpath,
                               )
    browser_profile1.add_tables_for_access(file=file_name,
                                           tables=[table_name], )
    urls_records_yielder = browser_profile1.access_fields(
            table='keyword_search_terms',
            fields=['keyword_id', 'url_id', 'lower_term', 'term']
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
    browser_two_profiles = Browser(browser='chrome',
                      profiles=['Profile 1', 'Profile 2'],
                      profile_root=profile_rootpath,
                      )
    browser_two_profiles.add_tables_for_access(file='History', tables=['urls'], )
    urls_records_yielder = browser_two_profiles.access_fields(
            table='urls',
            fields=['id', 'url', 'title',
                    'last_visit_time',
                    'last_visit_readable',
                    ]
        
            )
    profile_1_2_records_using_browser = [record for record in urls_records_yielder]
    sort_by_id = lambda item: item['id']
    profile_1_2_records_using_browser.sort(key=sort_by_id)

    profile1_table = Table(table='urls',
                            path=Path(profile_rootpath,
                                      'Profile 1',
                                      'History',
                                      ),
                           browser='chrome',
                            filename='History',
                            profile='Profile 1',
                            )
    profile1_table.make_records_yielder()
    profile1_records = list(profile1_table.records_yielder)
    
    profile2_table = Table(table='urls',
                            path=Path(profile_rootpath,
                                      'Profile 2',
                                      'History',
                                      ),
                           browser='chrome',
                            filename='History',
                            profile='Profile 2',
                            )
    profile2_table.make_records_yielder()
    profile2_records = list(profile2_table.records_yielder)
    
    profile_1_2_records_using_tables = [*profile1_records, *profile2_records]
    profile_1_2_records_using_tables.sort(key=sort_by_id)
    assert profile_1_2_records_using_tables == profile_1_2_records_using_tables

    
def test_browser_access_same_profile_file_two_tables(tests_root):
    browser_profile_1 = Browser(browser='chrome',
                                profiles=['Profile 1'],
                                profile_root=Path(tests_root, 'chrome_databases'),
                                file_tables={'History': ['urls', 'keyword_search_terms']}
                                )
    browser_profile_1 .add_tables_for_access(file='History', tables=['urls', 'keyword_search_terms'])
    
    urls_records_yielder = browser_profile_1.access_fields(
            table='urls', fields=['id', 'url', 'title',
                                        'last_visit_time',
                                        'last_visit_readable',
                                        ]
            )
    records_urls = [rec_mp for rec_mp in urls_records_yielder]

    keyword_search_terms_record_yielder = browser_profile_1.access_fields(
            table='keyword_search_terms',
            fields=['keyword_id', 'url_id', 'lower_term', 'term'],
            )
    records_keyword_search_terms = [rec_mo for rec_mo in keyword_search_terms_record_yielder]

    unique_urls = check_records_unique_with_field(
            records=records_urls,
            field='id',
            )
    unique_keyword_search_terms = check_records_unique_with_field(
            records=records_keyword_search_terms,
            field='url_id',
            )
    assert unique_urls
    assert unique_keyword_search_terms

    urls_actual_ids = [record['id'] for record in records_urls]
    keyword_search_terms_actual_ids = [record['url_id'] for record in records_keyword_search_terms]
    
    urls_expected_ids = list(range(1, 5))
    keyword_search_terms_expected_ids = [1, 3]
    
    assert urls_expected_ids == urls_actual_ids
    assert keyword_search_terms_expected_ids == keyword_search_terms_actual_ids

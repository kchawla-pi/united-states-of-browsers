from pathlib import Path

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
    
    browser_profile1 = Browser(browser=browser_name,
                      profiles=[profile_name],
                      profile_root=profile_rootpath,
                      )
    browser_profile1.add_tables_for_access(file=file_name, tables=[table_name], )
    moz_places_records_yielder = browser_profile1.access_fields(
            table='moz_places',
            fields=['id', 'url', 'title',
                    'last_visit_date',
                    'last_visit_readable',
                    ]
            )
    browser_profile1_records = [record for record in moz_places_records_yielder]
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
    profile_rootpath = Path(tests_root, 'firefox_databases')
    profile_path = Path(profile_rootpath,
                        't87e6f86.test_profile1',
                        'places.sqlite',
                        )
    browser_name = 'firefox'
    table_name = 'moz_origins'
    profile_name = 'test_profile1'
    file_name = 'places.sqlite'
    
    browser_profile1 = Browser(browser=browser_name,
                               profiles=[profile_name],
                               profile_root=profile_rootpath,
                               )
    browser_profile1.add_tables_for_access(file=file_name,
                                           tables=[table_name], )
    moz_places_records_yielder = browser_profile1.access_fields(
            table='moz_origins',
            fields=['id', 'prefix', 'host', 'frecency']
            )
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
    browser_two_profiles.add_tables_for_access(file='places.sqlite', tables=['moz_places'], )
    moz_places_records_yielder = browser_two_profiles.access_fields(
            table='moz_places',
            fields=['id', 'url', 'title',
                    'last_visit_date',
                    'last_visit_readable',
                    ]
        
            )
    profile_1_2_records_using_browser = [record for record in moz_places_records_yielder]
    sort_by_id = lambda item: item['id']
    profile_1_2_records_using_browser.sort(key=sort_by_id)

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
    profile_1_2_records_using_tables.sort(key=sort_by_id)
    assert profile_1_2_records_using_tables == profile_1_2_records_using_tables

    
def test_browser_access_same_profile_file_two_tables(tests_root):
    browser_profile_1 = Browser(browser='firefox',
                                profiles=['test_profile1'],
                                profile_root=Path(tests_root, 'firefox_databases'),
                                file_tables={'places.sqlite': ['moz_places', 'moz_origins']}
                                )
    browser_profile_1 .add_tables_for_access(file='places.sqlite', tables=['moz_places', 'moz_origins'])
    
    moz_places_records_yielder = browser_profile_1.access_fields(
            table='moz_places', fields=['id', 'url', 'title',
                                        'last_visit_date',
                                        'last_visit_readable',
                                        ]
            )
    records_moz_places = [rec_mp for rec_mp in moz_places_records_yielder]

    moz_origins_record_yielder = browser_profile_1.access_fields(
            table='moz_origins',
            fields=['id', 'prefix', 'host', 'frecency'],
            )
    records_moz_origins = [rec_mo for rec_mo in moz_origins_record_yielder]

    unique_moz_places = check_records_unique_with_field(
            records=records_moz_places,
            field='id',
            )
    unique_moz_origins = check_records_unique_with_field(
            records=records_moz_origins,
            field='id',
            )
    assert unique_moz_places
    assert unique_moz_origins

    moz_places_actual_ids = [record['id'] for record in records_moz_places]
    moz_origins_actual_ids = [record['id'] for record in records_moz_origins]
    
    moz_places_expected_ids = list(range(1, 19))
    moz_origins_expected_ids = list(range(1, 14))
    
    assert moz_places_expected_ids == moz_places_actual_ids
    assert moz_origins_expected_ids == moz_origins_actual_ids

from pathlib import Path

from united_states_of_browsers.db_merge.browser import Browser
from united_states_of_browsers.db_merge.table import Table


def test_browser_methods(tests_root):
    profile_rootpath = Path(tests_root, 'firefox_databases')
    browser_two_profiles = Browser(browser='firefox',
                      profiles=['test_profile1', 'test_profile2'],
                      profile_root=profile_rootpath,
                      )
    browser_two_profiles.add_tables_for_access(file='places.sqlite', tables=['moz_places'], )
    moz_places_records_yielder = browser_two_profiles.access_fields(
            {'moz_places': ['id', 'url', 'title',
                            'last_visit_date',
                            'last_visit_readable']
             }
            )
    # print(*list(moz_places_records_yielder), sep='\n')
    # quit()
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

    
        
def test_browser_methods_2(tests_root):
    browser_profile_1 = Browser(browser='firefox',
                      profiles=['test_profile1'],
                      profile_root=Path(tests_root, 'firefox_databases'),
                      )
    browser_profile_1 .add_tables_for_access(file='places.sqlite', tables=['moz_places'], )
    moz_places_records_yielder = browser_profile_1 .access_fields(
            {'moz_places': ['id', 'url', 'title',
                            'last_visit_date',
                            'last_visit_readable']
             }
            )
    # list(records_yielder)
    for rec in moz_places_records_yielder:
        print((rec))

        
        
if __name__ == '__main__':
    test_browser_methods(tests_root='/home/kshitij/workspace/united-states-of-browsers/tests')

from pathlib import Path

import pytest

from united_states_of_browsers.db_merge.db_merge import (
    BrowserData,
    DatabaseMergeOrchestrator,
    )


def _make_data_for_tests(tests_root):
    firefox_info = BrowserData(os='posix',
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

    chrome_info = BrowserData(os='posix',
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
    opera_info = BrowserData(os='posix',
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
    combined_db = DatabaseMergeOrchestrator(app_path=tests_root,
                                            db_name='test_combi_db',
                                            browser_info=browser_info,
                                            )
    return combined_db


def _make_expected_data():
    expected_data = {
        11: {'id': 12, 'url': 'http://www.linuxmint.com/start/tessa/',
             'title': None, 'visit_count': 1,
             'last_visit_date': 1567466430249670,
             'last_visit_readable': '2019-09-03 01:20:30',
             'browser': 'firefox',
             'profile': 't87e6f86.test_profile1', 'file': 'places.sqlite',
             'table': 'moz_places'
             },
        37: {'id': 20, 'url': 'https://www.youtube.com/', 'title': 'YouTube',
             'visit_count': 1, 'last_visit_date': 1567466777759963,
             'last_visit_readable': '2019-09-03 01:26:17',
             'browser': 'firefox', 'profile': 'z786c76dv78.test_profile2',
             'file': 'places.sqlite', 'table': 'moz_places'
             },
        44: {'id': 7,
             'url': 'https://www.google.com/search?q=about%3A+profiles+chrome&oq=about%3A+profiles+chrome&aqs=chrome..69i64.9800j1j8&sourceid=chrome&ie=UTF-8',
             'title': 'about: profiles chrome - Google Search',
             'visit_count': 1, 'last_visit_time': 13212130939811649,
             'last_visit_readable': '2388-09-04 05:22:19', 'browser': 'chrome',
             'profile': 'Profile 2', 'file': 'History', 'table': 'urls'
             },
        - 1: {'id': 4, 'url': 'https://circleci.com/',
              'title': 'Continuous Integration and Delivery - CircleCI',
              'visit_count': 1, 'last_visit_time': 13212132010525366,
              'last_visit_readable': '2388-09-04 05:40:10',
              'browser': 'chrome', 'profile': 'Profile 1',
              'file': 'History', 'table': 'urls'
              }
        }
    return expected_data

def test_find_installed_browsers(tests_root):
    combined_db = _make_data_for_tests(tests_root)
    assert combined_db.installed_browsers_data is None
    combined_db.find_installed_browsers()
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
    combined_db = _make_data_for_tests(tests_root)
    combined_db.find_installed_browsers()
    combined_db.make_records_yielders()
    combi_records = [browser_records
                      for browser_records_yielder in combined_db.browser_yielder
                      for browser_records in browser_records_yielder
                      ]
    # print(*combi_records, sep='\n')
    expected_data = _make_expected_data()
    assert expected_data[11] == combi_records[11]
    assert expected_data[37] == combi_records[37]
    assert expected_data[44] == combi_records[44]
    assert expected_data[-1] == combi_records[-1]


if __name__ == '__main__':
    tests_root = '/home/kshitij/workspace/united-states-of-browsers/tests'
    combined_db = _make_data_for_tests(tests_root)
    test_find_installed_browsers(combined_db)
    test_make_records_yielder(combined_db)


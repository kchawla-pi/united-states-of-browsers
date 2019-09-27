import tempfile

import pytest

from tests.unit_tests.test_db_merge import _make_data_for_tests
from united_states_of_browsers.db_merge.db_merge import \
    DatabaseMergeOrchestrator
from united_states_of_browsers.db_merge.db_search import (check_fts5_installed,
                                                          search,
                                                          )


pytestmark = pytest.mark.skipif(not check_fts5_installed(),
                                reason='FTS5 not available. Search disabled',
                                )

def test_search_with_keywords_and_dates(tests_root):
    browser_info = _make_data_for_tests(tests_root)
    with tempfile.TemporaryDirectory() as tmp_dir:
        combined_db = DatabaseMergeOrchestrator(app_path=tmp_dir,
                                                db_name='test_combi_db',
                                                browser_info=browser_info,
                                                )
        combined_db.orchestrate_db_merge()
        actual_search_results_rec_ids = {}
        search_keywords = ('circleci', 'google', 'gitlab')
        for search_keyword_ in search_keywords:
            actual_search_results_rec_ids[search_keyword_] = sorted([
                row['rec_id']
                for row in search(combined_db.output_db,
                                  word_query=search_keyword_,
                                  date_start='2019-01-01',
                                  date_stop='2388-12-31',
                                  )
                ])
        expected_search_results_rec_ids = {'circleci': [50, 51],
                                           'google': [32, 33, 45, 46, 48, 50],
                                           'gitlab': [42, 43, 44],
                                           }
        assert expected_search_results_rec_ids == actual_search_results_rec_ids


def test_search_dates_specified(tests_root):
    browser_info = _make_data_for_tests(tests_root)
    with tempfile.TemporaryDirectory() as tmp_dir:
        combined_db = DatabaseMergeOrchestrator(app_path=tmp_dir,
                                                db_name='test_combi_db',
                                                browser_info=browser_info,
                                                )
        combined_db.orchestrate_db_merge()

        expected_search_results_rec_ids = list(range(39, 52))
        actual_search_results_rec_ids = sorted([row['rec_id']
                                                for row in
                                                search(combined_db.output_db,
                                                       date_start='2388-09-01',
                                                       date_stop='2388-09-30',
                                                       )
                                                ])
        assert expected_search_results_rec_ids == actual_search_results_rec_ids


def test_search_keywords(tests_root):
    browser_info = _make_data_for_tests(tests_root)
    with tempfile.TemporaryDirectory() as tmp_dir:
        combined_db = DatabaseMergeOrchestrator(app_path=tmp_dir,
                                                db_name='test_combi_db',
                                                browser_info=browser_info,
                                                )
        combined_db.orchestrate_db_merge()

        expected_search_results_rec_ids = [13, 31]
        actual_search_results_rec_ids = sorted([row['rec_id']
                                                for row in
                                                search(
                                                    combined_db.output_db,
                                                        word_query='start page',
                                                    )
                                                ])
        assert expected_search_results_rec_ids == actual_search_results_rec_ids


def test_search_dates_till_now(tests_root):
    browser_info = _make_data_for_tests(tests_root)
    with tempfile.TemporaryDirectory() as tmp_dir:
        combined_db = DatabaseMergeOrchestrator(app_path=tmp_dir,
                                                db_name='test_combi_db',
                                                browser_info=browser_info,
                                                )
        combined_db.orchestrate_db_merge()

        rec_id_ranges = (10, 20), (29, 39)
        expected_search_results_rec_ids = [list(range(*rec_id_range_))
                                           for rec_id_range_ in rec_id_ranges
                                           ]
        expected_search_results_rec_ids = [*expected_search_results_rec_ids[0],
                                           *expected_search_results_rec_ids[1],
                                           ]
        actual_search_results_rec_ids = sorted([row['rec_id']
                                                for row in
                                                search(combined_db.output_db,)
                                                ])
        assert expected_search_results_rec_ids == actual_search_results_rec_ids


if __name__ == '__main__':
    tests_root = '/home/kshitij/workspace/united-states-of-browsers/tests'
    # test_search_with_keywords(tests_root)
    # test_search_dates_specified(tests_root)
    # test_search_dates_keywords(tests_root)
    # test_search_dates_till_now(tests_root)

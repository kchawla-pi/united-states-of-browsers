import pytest

from united_states_of_browsers.db_merge.db_search import (
    check_fts5_installed,
    search,
)


pytestmark = pytest.mark.skipif(
    not check_fts5_installed(),
    reason="FTS5 not available. Search disabled",
)


def test_search_with_keywords_and_dates(searchable_db_path):
    actual_search_results_rec_ids = {}
    search_keywords = ("circleci", "google", "gitlab")
    for search_keyword_ in search_keywords:
        actual_search_results_rec_ids[search_keyword_] = sorted(
            [
                row["rec_id"]
                for row in search(
                    searchable_db_path,
                    word_query=search_keyword_,
                    date_start="2019-01-01",
                    date_stop="2388-12-31",
                )
            ]
        )
    expected_search_results_rec_ids = {
        "circleci": [50, 51],
        "google": [32, 33, 45, 46, 48, 50],
        "gitlab": [42, 43, 44],
    }
    assert expected_search_results_rec_ids == actual_search_results_rec_ids


def test_search_dates_specified(searchable_db_path):
    expected_search_results_rec_ids = list(range(39, 52))
    actual_search_results_rec_ids = sorted(
        [
            row["rec_id"]
            for row in search(
                searchable_db_path,
                date_start="2388-09-01",
                date_stop="2388-09-30",
            )
        ]
    )
    assert expected_search_results_rec_ids == actual_search_results_rec_ids


def test_search_keywords(searchable_db_path):
    expected_search_results_rec_ids = [13, 31]
    actual_search_results_rec_ids = sorted(
        [
            row["rec_id"]
            for row in search(
                searchable_db_path,
                word_query="start page",
            )
        ]
    )
    assert expected_search_results_rec_ids == actual_search_results_rec_ids


def test_search_dates_till_now(searchable_db_path):
    expected_search_results_rec_ids = [*range(10, 20), *range(29, 39)]
    actual_search_results_rec_ids = sorted(
        [
            row["rec_id"]
            for row in search(
                searchable_db_path,
            )
        ]
    )
    assert expected_search_results_rec_ids == actual_search_results_rec_ids


def test_search_date_start(searchable_db_path):
    expected_search_results_rec_ids = []
    actual_search_results_rec_ids = sorted(
        [
            row["rec_id"]
            for row in search(
                searchable_db_path,
                date_start="2388-09-01",
            )
        ]
    )
    assert expected_search_results_rec_ids == actual_search_results_rec_ids


def test_search_date_stop(searchable_db_path):
    expected_search_results_rec_ids = [*range(10, 20), *range(29, 39)]
    actual_search_results_rec_ids = sorted(
        [
            row["rec_id"]
            for row in search(
                searchable_db_path,
                date_stop="2019-09-04",
            )
        ]
    )
    assert expected_search_results_rec_ids == actual_search_results_rec_ids

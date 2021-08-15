import sqlite3
from pathlib import Path
from pprint import pprint

import pytest

from united_states_of_browsers.db_merge import TableAccessError
from united_states_of_browsers.db_merge.browser import (
    make_browser_records_yielder,
    make_browser_paths,
)
from united_states_of_browsers.db_merge.helpers import check_records_unique_with_field
from united_states_of_browsers.db_merge.table import Table


def test_firefox_invalid_profileroot(tests_root):
    profile_rootpath = Path(tests_root, "firefox_databases_JUNK")
    browser_name = "firefox"
    table_name = "moz_places"
    profile_name = "test_profile1"
    file_name = "places.sqlite_JUNK"
    moz_places_records_yielder = make_browser_records_yielder(
        browser=browser_name,
        profile_root=profile_rootpath,
        filename=file_name,
        tablename=table_name,
        profiles=[profile_name],
    )
    with pytest.raises(FileNotFoundError):
        list(moz_places_records_yielder)


def test_firefox_invalid_proflie(tests_root):
    profile_rootpath = Path(tests_root, "firefox_databases")
    browser_name = "firefox"
    table_name = "moz_places"
    profile_name = ["test_profile1_JUNK"]
    file_name = "places.sqlite"
    actual_browser_paths = make_browser_paths(
        browser=browser_name,
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


def test_firefox_two_proflies_one_invalid(tests_root):
    profile_rootpath = Path(tests_root, "firefox_databases")
    browser_name = "firefox"
    table_name = "moz_places"
    profile_names = ["test_profile1_JUNK", "test_profile2"]
    file_name = "places.sqlite"
    expected_browser_paths = {
        "test_profile2": Path(profile_rootpath, "z786c76dv78.test_profile2")
    }
    actual_browser_paths = make_browser_paths(
        browser=browser_name,
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
    assert expected_browser_paths == actual_browser_paths
    assert len(actual_records) == 20
    assert [record["id"] for record in actual_records] == list(range(1, 21))
    assert actual_records[0]["url"] == "http://www.linuxmint.com/start/tessa"
    assert actual_records[-1]["id"] == 20
    assert actual_records[-1]["url"] == "https://www.youtube.com/"


def test_firefox_invalid_file(tests_root):
    profile_rootpath = Path(tests_root, "firefox_databases")
    browser_name = "firefox"
    table_name = "moz_places"
    profile_name = ["test_profile1"]
    file_name = "places.sqlite_JUNK"
    moz_places_records_yielder = make_browser_records_yielder(
        browser=browser_name,
        profile_root=profile_rootpath,
        filename=file_name,
        tablename=table_name,
        profiles=profile_name,
    )
    with pytest.raises(sqlite3.OperationalError):
        list(moz_places_records_yielder)


def test_firefox_invalid_table(tests_root):
    profile_rootpath = Path(tests_root, "firefox_databases")
    browser_name = "firefox"
    table_name = "moz_places_JUNK"
    profile_name = ["test_profile1"]
    file_name = "places.sqlite"
    moz_places_records_yielder = make_browser_records_yielder(
        browser=browser_name,
        profile_root=profile_rootpath,
        filename=file_name,
        tablename=table_name,
        profiles=profile_name,
    )
    with pytest.raises(TableAccessError):
        list(moz_places_records_yielder)


def test_chrome_invalid_profileroot(tests_root):
    profile_rootpath = Path(tests_root, "chrome_databases_JUNK")
    browser_name = "chrome"
    table_name = "urls"
    profile_name = "Profile 1"
    file_name = "History"
    moz_places_records_yielder = make_browser_records_yielder(
        browser=browser_name,
        profile_root=profile_rootpath,
        filename=file_name,
        tablename=table_name,
        profiles=[profile_name],
    )
    with pytest.raises(FileNotFoundError):
        list(moz_places_records_yielder)


def test_chrome_invalid_proflie(tests_root):
    profile_rootpath = Path(tests_root, "chrome_databases")
    browser_name = "chrome"
    table_name = "urls"
    profile_name = ["Profile 1 JUNK"]
    file_name = "History"
    actual_browser_paths = make_browser_paths(
        browser=browser_name,
        profile_root=profile_rootpath,
        profiles=profile_name,
    )
    urls_records_yielder = make_browser_records_yielder(
        browser=browser_name,
        profile_root=profile_rootpath,
        filename=file_name,
        tablename=table_name,
        profiles=profile_name,
    )
    yielded_records = list(urls_records_yielder)
    assert actual_browser_paths == {}
    assert yielded_records == []


def test_chrome_two_proflies_one_invalid(tests_root):
    profile_rootpath = Path(tests_root, "chrome_databases")
    browser_name = "chrome"
    table_name = "urls"
    profile_names = ["Profile 1 JUNK", "Profile 2"]
    file_name = "History"
    expected_browser_paths = {"Profile 2": Path(profile_rootpath, "Profile 2")}
    actual_browser_paths = make_browser_paths(
        browser=browser_name,
        profile_root=profile_rootpath,
        profiles=profile_names,
    )
    urls_records_yielder = make_browser_records_yielder(
        browser=browser_name,
        profile_root=profile_rootpath,
        filename=file_name,
        tablename=table_name,
        profiles=profile_names,
    )
    actual_records = list(urls_records_yielder)
    assert expected_browser_paths == actual_browser_paths
    assert len(actual_records) == 9
    assert [record["id"] for record in actual_records] == list(range(1, 10))
    assert actual_records[5]["id"] == 6
    assert actual_records[5]["url"] == "https://about.gitlab.com/"
    assert actual_records[-1]["id"] == 9
    assert (
        actual_records[-1]["url"]
        == "https://www.howtogeek.com/255653/how-to-find-your-chrome-profile-folder-on-windows-mac-and-linux/"
    )


def test_chrome_invalid_file(tests_root):
    profile_rootpath = Path(tests_root, "chrome_databases")
    browser_name = "chrome"
    table_name = "urls"
    profile_name = "Profile 1"
    file_name = "History JUNK"
    urls_records_yielder = make_browser_records_yielder(
        browser=browser_name,
        profile_root=profile_rootpath,
        filename=file_name,
        tablename=table_name,
        profiles=[profile_name],
    )
    with pytest.raises(sqlite3.OperationalError):
        list(urls_records_yielder)


def test_chrome_invalid_table(tests_root):
    profile_rootpath = Path(tests_root, "chrome_databases")
    browser_name = "chrome"
    table_name = "urls_JUNK"
    profile_name = "Profile 1"
    file_name = "History"
    urls_records_yielder = make_browser_records_yielder(
        browser=browser_name,
        profile_root=profile_rootpath,
        filename=file_name,
        tablename=table_name,
        profiles=[profile_name],
    )
    with pytest.raises(TableAccessError):
        print(list(urls_records_yielder))


if __name__ == "__main__":
    tests_root = "/home/kshitij/workspace/united-states-of-browsers/tests"
    # test_firefox_two_proflies_one_missing(tests_root)
    # test_firefox_access_single_profile_file_table_with_timestamp(tests_root)
    # test_firefox_missing_proflie(tests_root)
    # test_firefox_missing_path_1(tests_root)
    # test_firefox_missing_path_2(tests_root)

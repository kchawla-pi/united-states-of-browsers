from pathlib import Path

from united_states_of_browsers.db_merge.browser import make_browser_paths


def test_browser_firefox_make_paths_during_init_one_profile(tests_root):
    profile_rootpath = Path(tests_root, "firefox_databases")
    browser_name = "firefox"
    profile_name = "test_profile1"

    profile1_browser_paths = make_browser_paths(
        browser=browser_name,
        profile_root=profile_rootpath,
        profiles=[profile_name],
    )
    expected_paths = {"test_profile1": Path(profile_rootpath, "t87e6f86.test_profile1")}

    assert profile1_browser_paths.keys() == expected_paths.keys()

    for profile_name in profile1_browser_paths:
        assert profile1_browser_paths[profile_name] == expected_paths[profile_name]


def test_browser_firefox_make_paths_during_init_two_profiles(tests_root):
    profile_rootpath = Path(tests_root, "firefox_databases")
    browser_name = "firefox"
    profile_names = ["test_profile1", "test_profile2"]

    browser_profile1 = make_browser_paths(
        browser=browser_name,
        profile_root=profile_rootpath,
        profiles=profile_names,
    )
    expected_paths = {
        "test_profile1": Path(profile_rootpath, "t87e6f86.test_profile1"),
        "test_profile2": Path(profile_rootpath, "z786c76dv78.test_profile2"),
    }

    assert browser_profile1.keys() == expected_paths.keys()

    for profile_name in browser_profile1:
        assert browser_profile1[profile_name] == expected_paths[profile_name]


def test_browser_firefox_make_paths_during_init_all_profiles(tests_root):
    profile_rootpath = Path(tests_root, "firefox_databases")
    browser_name = "firefox"
    profile_names = None

    browser_profile1 = make_browser_paths(
        browser=browser_name,
        profile_root=profile_rootpath,
        profiles=profile_names,
    )
    expected_paths = {
        "test_profile1": Path(profile_rootpath, "t87e6f86.test_profile1"),
        "test_profile2": Path(profile_rootpath, "z786c76dv78.test_profile2"),
    }

    assert browser_profile1.keys() == expected_paths.keys()

    for profile_name in browser_profile1:
        assert browser_profile1[profile_name] == expected_paths[profile_name]


def test_browser_chrome_make_paths_during_init_one_profile(tests_root):
    profile_rootpath = Path(tests_root, "chrome_databases")
    browser_name = "chrome"
    profile_name = "Profile 1"

    browser_profile1 = make_browser_paths(
        browser=browser_name,
        profile_root=profile_rootpath,
        profiles=[profile_name],
    )
    expected_paths = {"Profile 1": Path(profile_rootpath, "Profile 1")}

    assert browser_profile1.keys() == expected_paths.keys()

    for profile_name in browser_profile1:
        assert browser_profile1[profile_name] == expected_paths[profile_name]


def test_browser_chrome_make_paths_during_init_two_profiles(tests_root):
    profile_rootpath = Path(tests_root, "chrome_databases")
    browser_name = "chrome"
    profile_names = ["Profile 1", "Profile 2"]

    browser_profile1 = make_browser_paths(
        browser=browser_name,
        profile_root=profile_rootpath,
        profiles=profile_names,
    )
    expected_paths = {
        "Profile 1": Path(profile_rootpath, "Profile 1"),
        "Profile 2": Path(profile_rootpath, "Profile 2"),
    }

    assert browser_profile1.keys() == expected_paths.keys()

    for profile_name in browser_profile1:
        assert browser_profile1[profile_name] == expected_paths[profile_name]


def test_browser_chrome_make_paths_during_init_all_profiles(tests_root):
    profile_rootpath = Path(tests_root, "chrome_databases")
    browser_name = "chrome"
    profile_names = None

    browser_profile1 = make_browser_paths(
        browser=browser_name,
        profile_root=profile_rootpath,
        profiles=profile_names,
    )
    expected_paths = {
        "Profile 1": Path(profile_rootpath, "Profile 1"),
        "Profile 2": Path(profile_rootpath, "Profile 2"),
    }

    assert browser_profile1.keys() == expected_paths.keys()

    for profile_name in browser_profile1:
        assert browser_profile1[profile_name] == expected_paths[profile_name]


if __name__ == "__main__":  # pragma: no cover
    tests_root = "/home/kshitij/workspace/united-states-of-browsers/tests"
    test_browser_firefox_make_paths_during_init_all_profiles(tests_root)

# def test_make_browser_paths():
#     files = ['places.sqlite', 'permissions.sqlite']
#     firefox_all = make_browser_paths(browser='firefox',
#                                profile_root='~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles')
#     firefox_all.make_browser_paths()
#
#     profiles_list = ['test_profile0', 'test_profile1']
#     firefox_some = make_browser_paths(browser='firefox',
#                                 profile_root='~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles',
#                                 profiles=profiles_list)
#     firefox_some.make_browser_paths()
#
#     chrome = make_browser_paths(browser='chrome',
#                           profile_root='C:\\Users\\kshit\\AppData\\Local\\Google\\Chrome\\User Data')
#
#     objects_list = [firefox_all, firefox_some]

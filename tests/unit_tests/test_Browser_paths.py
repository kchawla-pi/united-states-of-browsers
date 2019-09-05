from pathlib import Path

from united_states_of_browsers.db_merge.browser import Browser


def test_browser_firefox_make_paths_during_init_one_profile(tests_root):
    profile_rootpath = Path(tests_root, 'firefox_databases')
    browser_name = 'firefox'
    profile_name = 'test_profile1'
    
    browser_profile1 = Browser(browser=browser_name,
                               profiles=[profile_name],
                               profile_root=profile_rootpath,
                               )
    expected_paths = {
        'test_profile1': Path(profile_rootpath, 't87e6f86.test_profile1')
        }
    
    assert browser_profile1.paths.keys() == expected_paths.keys()
    
    for profile_name in browser_profile1.paths:
        assert browser_profile1.paths[profile_name] == expected_paths[
            profile_name]


def test_browser_firefox_make_paths_during_init_two_profiles(tests_root):
    profile_rootpath = Path(tests_root, 'firefox_databases')
    browser_name = 'firefox'
    profile_names = ['test_profile1', 'test_profile2']
    
    browser_profile1 = Browser(browser=browser_name,
                               profiles=profile_names,
                               profile_root=profile_rootpath,
                               )
    expected_paths = {
        'test_profile1': Path(profile_rootpath, 't87e6f86.test_profile1'),
        'test_profile2': Path(profile_rootpath, 'z786c76dv78.test_profile2'),
        }
    
    assert browser_profile1.paths.keys() == expected_paths.keys()
    
    for profile_name in browser_profile1.paths:
        assert browser_profile1.paths[profile_name] == expected_paths[
            profile_name]


def test_browser_firefox_make_paths_during_init_all_profiles(tests_root):
    profile_rootpath = Path(tests_root, 'firefox_databases')
    browser_name = 'firefox'
    profile_names = None
    
    browser_profile1 = Browser(browser=browser_name,
                               profiles=profile_names,
                               profile_root=profile_rootpath,
                               )
    expected_paths = {
        'test_profile1': Path(profile_rootpath, 't87e6f86.test_profile1'),
        'test_profile2': Path(profile_rootpath, 'z786c76dv78.test_profile2'),
        }
    
    assert browser_profile1.paths.keys() == expected_paths.keys()
    
    for profile_name in browser_profile1.paths:
        assert browser_profile1.paths[profile_name] == expected_paths[
            profile_name]


def test_browser_chrome_make_paths_during_init_one_profile(tests_root):
    profile_rootpath = Path(tests_root, 'chrome_databases')
    browser_name = 'chrome'
    profile_name = 'Profile 1'
    
    browser_profile1 = Browser(browser=browser_name,
                               profiles=[profile_name],
                               profile_root=profile_rootpath,
                               )
    expected_paths = {'Profile 1': Path(profile_rootpath, 'Profile 1')}
    
    assert browser_profile1.paths.keys() == expected_paths.keys()
    
    for profile_name in browser_profile1.paths:
        assert browser_profile1.paths[profile_name] == expected_paths[
            profile_name]


def test_browser_chrome_make_paths_during_init_two_profiles(tests_root):
    profile_rootpath = Path(tests_root, 'chrome_databases')
    browser_name = 'chrome'
    profile_names = ['Profile 1', 'Profile 2']
    
    browser_profile1 = Browser(browser=browser_name,
                               profiles=profile_names,
                               profile_root=profile_rootpath,
                               )
    expected_paths = {'Profile 1': Path(profile_rootpath, 'Profile 1'),
                      'Profile 2': Path(profile_rootpath, 'Profile 2'),
                      }
    
    assert browser_profile1.paths.keys() == expected_paths.keys()
    
    for profile_name in browser_profile1.paths:
        assert browser_profile1.paths[profile_name] == expected_paths[
            profile_name]


def test_browser_chrome_make_paths_during_init_all_profiles(tests_root):
    profile_rootpath = Path(tests_root, 'chrome_databases')
    browser_name = 'chrome'
    profile_names = None
    
    browser_profile1 = Browser(browser=browser_name,
                               profiles=profile_names,
                               profile_root=profile_rootpath,
                               )
    expected_paths = {'Profile 1': Path(profile_rootpath, 'Profile 1'),
                      'Profile 2': Path(profile_rootpath, 'Profile 2'),
                      }
    
    assert browser_profile1.paths.keys() == expected_paths.keys()
    
    for profile_name in browser_profile1.paths:
        assert browser_profile1.paths[profile_name] == expected_paths[
            profile_name]

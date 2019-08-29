import pytest

from united_states_of_browsers.db_merge.helpers import get_root_path


def test_get_root_path():
    root_path_single = get_root_path(
            'C:/Users/kshit/OneDrive\workspace/UnitedStatesOfBrowsers/tests/unit_tests/tester_classes',
            'UnitedStatesOfBrowsers')
    assert root_path_single == 'C:/Users/kshit/OneDrive\workspace/UnitedStatesOfBrowsers'
    
    root_path_double = get_root_path(
            'C:/Users/kshit/OneDrive\workspace/UnitedStatesOfBrowsers/tests/UnitedStatesOfBrowsers/tester_classes',
            'UnitedStatesOfBrowsers')
    assert root_path_double == 'C:/Users/kshit/OneDrive\workspace/UnitedStatesOfBrowsers'
    
    root_path_hyphen = get_root_path(
            '/home/kshitij/workspace/united-states-of-browsers/tests/unit_tests/test_helpers/test_get_root_path.py',
            'united-states-of-browsers')
    assert root_path_hyphen == '/home/kshitij/workspace/united-states-of-browsers'


def test_get_root_path_incorrect_path():
    with pytest.raises(ValueError):
        root_path_hyphen = get_root_path(
                '/home/kshitij/workspace/united-states-of-browsers/tests/unit_tests/test_helpers/test_get_root_path.py',
                'UnitedStatesOfBrowsers')

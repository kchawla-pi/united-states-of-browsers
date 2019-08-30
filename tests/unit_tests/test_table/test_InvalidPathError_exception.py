from pathlib import Path

import pytest

from united_states_of_browsers.db_merge.table import Table


def test_InvalidPathError_mozilla(tests_root):
    table_obj = Table(table='moz_places',
                      path=Path(tests_root,
                                'data/browser_profiles_for_testing_wrongpath_/AppData/Roaming/Mozilla/'
                                'Firefox/Profiles/kceyj748.test_profile1/places.sqlite'),
                      browser='firefox',
                      filename='places.sqlite',
                      profile='test_profile1',
                      copies_subpath=None,
                      )
    with pytest.raises(OSError) as excep:
        table_obj.make_records_yielder()


def test_InvalidPathError_chrome(tests_root):
    table_obj = Table(table='urls',
                      path=Path(tests_root,
                                'data/browser_profiles_for_testing/AppData/Local/Google/Chrome/User Data/Profile 1 _wrongpath_/History'),
                      browser='chrome',
                      filename='History',
                      profile='Profile 1 _wrongpath_',
                      copies_subpath=None,
                      )
    with pytest.raises(OSError) as excep:
        table_obj.make_records_yielder()


def test_InvalidPathError_vivaldi(tests_root):
    table_obj = Table(table='urls',
                      path=Path(tests_root,
                                'data/browser_profiles_for_testing/AppData/Local/Vivaldi/User_wrongpath_ Data/Default/History'),
                      browser='vivaldi',
                      filename='History',
                      profile='Default',
                      copies_subpath=None,
                      )
    with pytest.raises(OSError) as excep:
        table_obj.make_records_yielder()


def test_InvalidPathError_opera(tests_root):
    table_obj = Table(table='urls',
                      path=Path(tests_root,
                                'data/browser_profiles_for_testing/AppData_wrongpath_/Roaming/Opera Software/Opera Stable/History'),
                      browser='opera',
                      filename='History',
                      profile='Opera Stable',
                      copies_subpath=None,
                      )
    with pytest.raises(OSError) as excep:
        table_obj.make_records_yielder()

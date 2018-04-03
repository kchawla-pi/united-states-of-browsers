from pathlib import Path

from . import test_table as tt


test_cases_no_excep = [
	tt.TableArgs(table='urls',
	             path=Path(
			             'tests/data/browser_profiles_for_testing/AppData/Local/Google/Chrome/User Data/Profile 1/History'),
	             browser='chrome',
	             filename='History',
	             profile='Profile 1',
	             copies_subpath=None,
	             empty=False,
	             ),
	tt.TableArgs(table='urls',
	             path=Path(
			             'tests/data/browser_profiles_for_testing/AppData/Local/Vivaldi/User Data/Default/History'),
	             browser='vivaldi',
	             filename='History',
	             profile='Default',
	             copies_subpath=None,
	             empty=False,
	             ),
	tt.TableArgs(table='urls',
	             path=Path(
			             'tests/data/browser_profiles_for_testing/AppData/Roaming/Opera Software/Opera Stable/History'),
	             browser='opera',
	             filename='History',
	             profile='Opera Stable',
	             copies_subpath=None,
	             empty=False,
	             ),
	tt.TableArgs(table='moz_places',
	             path=Path(
			             'tests/data/browser_profiles_for_testing/AppData/Roaming/Mozilla/'
			             'Firefox/Profiles/e0pj4lec.test_profile0/places.sqlite'),
	             browser='firefox',
	             filename='places.sqlite',
	             profile='test_profile0',
	             copies_subpath=None,
	             empty=False,
	             ),
	tt.TableArgs(table='moz_places',
	             path=Path(
			             'tests/data/browser_profiles_for_testing/AppData/Roaming/Mozilla/'
			             'Firefox/Profiles/kceyj748.test_profile1/places.sqlite'),
	             browser='firefox',
	             filename='places.sqlite',
	             profile='test_profile1',
	             copies_subpath=None,
	             empty=False,
	             ),
	
	]

test_cases_exception_no_such_table = [tt.TableArgs(table='moz_places',
                                                    path=Path(
		                                                    'tests/data/browser_profiles_for_testing/AppData/Roaming/Mozilla/'
		                                                    'Firefox/Profiles/udd5sttq.test_profile2/places.sqlite'),
                                                    browser='firefox',
                                                    filename='places.sqlite',
                                                    profile='test_profile2',
                                                    copies_subpath=None,
                                                    empty=True,
                                                    ),
                                       ]

test_cases_exception_unable_to_open_database_file = [tt.TableArgs(table='moz_places',
                                      path=Path(
		                                      'tests/data/browser_profiles_for_testing/AppData/Roaming/Mozilla/'
		                                      'Firefox/Profiles/udd5sttq.test_profile2/places.sqlite'),
                                      browser='firefox',
                                      filename='places.sqlite',
                                      profile='test_profile2',
                                      copies_subpath=None,
                                      empty=True,
                                      ),
                         ]

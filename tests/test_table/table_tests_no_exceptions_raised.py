from pathlib import Path
from pprint import pprint

import test_table as tt

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

project_root = Path(__file__).parents[2]
for table_arg_no_excep in test_cases_no_excep:
	table_no_excep = tt.TestTable(project_root, table_arg_no_excep)
	print('Passed:', tt.test_suite_no_exceptions_raised(table_no_excep, True))

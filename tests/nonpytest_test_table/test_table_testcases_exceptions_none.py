from pathlib import Path

from tests.nonpytest_test_table import table_tester as tt

# from . import nonpytest_test_table as tt

project_root = Path(__file__).parents[2]

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


def test_suite_no_exceptions(table_tester_obj):
	test_results = [str(table_tester_obj),
	                table_tester_obj.test_connect(),
	                table_tester_obj.test_yield_readable_timestamps(),
	                table_tester_obj.test_get_records(),
	                table_tester_obj.test_check_if_db_empty(),
	                ]
	return test_results


def test_Table_no_exceptions():
	for table_arg_no_excep in test_cases_no_excep:
		table_no_excep = tt.TableTester(project_root, table_arg_no_excep)
		print('Passed:', test_suite_no_exceptions(table_no_excep))
		
		
if __name__ == '__main__':
	test_Table_no_exceptions()

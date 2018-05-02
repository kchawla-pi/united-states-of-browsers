import pytest

from pathlib import Path

from tests.tester_classes import table_tester as tt


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

@pytest.mark.parametrize('table_tester_obj', [tt.TableTester(project_root, test_case_) for test_case_ in test_cases_no_excep])
def test_suite_no_exceptions(table_tester_obj):
	test_results = [str(table_tester_obj),
	                table_tester_obj.test_connect(),
	                table_tester_obj.test_yield_readable_timestamps(),
	                table_tester_obj.test_get_records(),
	                table_tester_obj.test_check_if_db_empty(),
	                ]
	return test_results

def non_pytest_test_suite_no_exceptions():

	def test_Table_no_exceptions():
		for table_arg_no_excep in test_cases_no_excep:
			table_no_excep = tt.TableTester(project_root, table_arg_no_excep)
			print('Passed:', test_suite_no_exceptions(table_no_excep))
			
	test_Table_no_exceptions()


if __name__ == '__main__':
	non_pytest_test_suite_no_exceptions()

from tests.fixtures import (create_chromium_data,
							create_mozilla_data,
							get_project_root_path,
							)
from united_states_of_browsers.db_merge.table import Table

project_root = get_project_root_path()




def test_suite_no_exceptions_chromium():
	chromium_db_path = create_chromium_data()
	table_obj = Table(table='urls',
		             path=chromium_db_path,
		             browser='chrome',
		             filename='History',
		             profile='Profile 1',
		             copies_subpath=None,
		             )
	table_obj.make_records_yielder()
	for entry in table_obj.records_yielder:
		entry
	
	
def test_suite_no_exceptions_mozilla():
	mozilla_db_path = create_mozilla_data()
	table_obj = Table(table='moz_places',
	             path=mozilla_db_path,
	             browser='firefox',
	             filename='places.sqlite',
	             profile='test_profile0',
	             copies_subpath=None,
	             )
	table_obj.make_records_yielder()
	for entry in table_obj.records_yielder:
		entry


#
# test_cases_no_exception = [
# 	tt.TableArgs(table='urls',
# 	             path=Path(
# 			             'tests/data/browser_profiles_for_testing/AppData/Local/Google/Chrome/User Data/Profile 1/History'),
# 	             browser='chrome',
# 	             filename='History',
# 	             profile='Profile 1',
# 	             copies_subpath=None,
# 	             empty=False,
# 	             ),
# 	tt.TableArgs(table='urls',
# 	             path=Path(
# 			             'tests/data/browser_profiles_for_testing/AppData/Local/Vivaldi/User Data/Default/History'),
# 	             browser='vivaldi',
# 	             filename='History',
# 	             profile='Default',
# 	             copies_subpath=None,
# 	             empty=False,
# 	             ),
# 	tt.TableArgs(table='urls',
# 	             path=Path(
# 			             'tests/data/browser_profiles_for_testing/AppData/Roaming/Opera Software/Opera Stable/History'),
# 	             browser='opera',
# 	             filename='History',
# 	             profile='Opera Stable',
# 	             copies_subpath=None,
# 	             empty=False,
# 	             ),
# 	tt.TableArgs(table='moz_places',
# 	             path=Path(
# 			             'tests/data/browser_profiles_for_testing/AppData/Roaming/Mozilla/'
# 			             'Firefox/Profiles/e0pj4lec.test_profile0/places.sqlite'),
# 	             browser='firefox',
# 	             filename='places.sqlite',
# 	             profile='test_profile0',
# 	             copies_subpath=None,
# 	             empty=False,
# 	             ),
# 	tt.TableArgs(table='moz_places',
# 	             path=Path(
# 			             'tests/data/browser_profiles_for_testing/AppData/Roaming/Mozilla/'
# 			             'Firefox/Profiles/kceyj748.test_profile1/places.sqlite'),
# 	             browser='firefox',
# 	             filename='places.sqlite',
# 	             profile='test_profile1',
# 	             copies_subpath=None,
# 	             empty=False,
# 	             ),
# 	]
#
# @pytest.mark.parametrize('table_tester_obj', [tt.TableTester(project_root, test_case_) for test_case_ in test_cases_no_exception])
# def test_suite_no_exceptions(table_tester_obj):
# 	test_results = [str(table_tester_obj),
# 	                table_tester_obj.test_connect(),
# 	                table_tester_obj.test_yield_readable_timestamps(),
# 	                table_tester_obj.test_get_records(),
# 	                table_tester_obj.test_check_if_db_empty(),
# 	                ]
# 	return test_results
#
# def non_pytest_test_suite_no_exceptions(test_suite):
#
# 	def test_Table_no_exceptions(test_suite):
# 		for table_arg_no_excep in test_cases_no_exception:
# 			table_no_excep = tt.TableTester(project_root, table_arg_no_excep)
# 			print('Passed:', test_suite_no_exceptions(table_no_excep))
#
# 	test_Table_no_exceptions(test_suite=test_suite)
#
#
# if __name__ == '__main__':
# 	non_pytest_test_suite_no_exceptions(test_suite=test_cases_no_exception)

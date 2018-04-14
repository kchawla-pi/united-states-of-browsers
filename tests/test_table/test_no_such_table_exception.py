import pytest
import sqlite3

from pathlib import Path

from tests.tester_classes import table_tester as tt

project_root = Path(__file__).parents[2]

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
                                      tt.TableArgs(table='nonexistent_table',
                                                   path=Path(
		                                                   'tests/data/browser_profiles_for_testing/AppData/Local/Google/Chrome/User Data/Profile 1/History'),
                                                   browser='chrome',
                                                   filename='History',
                                                   profile='Profile 1',
                                                   copies_subpath=None,
                                                   empty=False,
                                                   ),
                                      tt.TableArgs(table='nonexistent_table',
                                                   path=Path(
		                                                   'tests/data/browser_profiles_for_testing/AppData/Local/Vivaldi/User Data/Default/History'),
                                                   browser='vivaldi',
                                                   filename='History',
                                                   profile='Default',
                                                   copies_subpath=None,
                                                   empty=False,
                                                   ),
                                      tt.TableArgs(table='nonexistent_table',
                                                   path=Path(
		                                                   'tests/data/browser_profiles_for_testing/AppData/Roaming/Opera Software/Opera Stable/History'),
                                                   browser='opera',
                                                   filename='History',
                                                   profile='Opera Stable',
                                                   copies_subpath=None,
                                                   empty=False,
                                                   ),
                                      # tt.TableArgs(table='moz_places',
                                      #              path=Path(
                                      #                     'tests/data/browser_profiles_for_testing/AppData/Roaming/Mozilla/'
                                      #                     'Firefox/Profiles/e0pj4lec.test_profile0/places.sqlite'),
                                      #              browser='firefox',
                                      #              filename='places.sqlite',
                                      #              profile='test_profile0',
                                      #              copies_subpath=None,
                                      #              empty=False,
                                      #              ),
                                      ]


def get_methods_to_be_tested(table_tester_obj):
	methods_to_be_tested = [
		table_tester_obj.test_connect,
		table_tester_obj.test_yield_readable_timestamps,
		table_tester_obj.test_get_records,
		# table_tester_obj.test_check_if_db_empty
		]
	return methods_to_be_tested


@pytest.mark.parametrize('table_tester_obj', [tt.TableTester(project_root, test_case_) for test_case_ in
                                              test_cases_exception_no_such_table]
                         )
def test_exception_no_such_table(table_tester_obj):
	methods_to_be_tested = get_methods_to_be_tested(table_tester_obj)
	for method_being_tested in methods_to_be_tested:
		with pytest.raises(
				sqlite3.OperationalError) as expected_exception:
			method_being_tested()
			if expected_exception:
				assert str(expected_exception) == f'no such tables: {table_tester_obj.test_data.table}'


def run_tests_without_pytest():
	def test_exception_no_such_table(table_tester_obj):
		methods_to_be_tested = get_methods_to_be_tested(table_tester_obj)
		for method_being_tested in methods_to_be_tested:
			try:
				result = method_being_tested()
			except sqlite3.OperationalError as excep:
				assert excep.args[0] == f'no such table: {table_tester_obj.test_data.table}'
			else:
				print(f'Expected exception not raised by method: {result}')
		return 'exception: no such table'
	
	def test_Table_exceptions_no_such_table():
		for table_arg_exception_ in test_cases_exception_no_such_table:
			table_obj = tt.TableTester(project_root, table_arg_exception_)
			print('Passed:', test_exception_no_such_table(table_obj))
	
	test_Table_exceptions_no_such_table()


if __name__ == '__main__':
	run_tests_without_pytest()

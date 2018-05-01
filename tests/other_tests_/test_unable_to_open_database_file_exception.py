import sqlite3
import pytest

from pathlib import Path
from tests.tester_classes import table_tester as tt

project_root = Path(__file__).parents[2]

test_cases_exception_unable_to_open_database_file = [tt.TableArgs(table='moz_places',
                                                                  path=Path(
		                                                                  'tests/data/browser_profiles_for_testing/AppData/Roaming/Mozilla/'
		                                                                  'Firefox/Profiles/udd5sttq.test_profile2/non_db_dummy_file_for_testing.txt'),
                                                                  browser='firefox',
                                                                  filename='non_db_dummy_file_for_testing.txt',
                                                                  profile='test_profile2',
                                                                  copies_subpath=None,
                                                                  empty=True,
                                                                  ),
                                                     ]


def get_methods_to_be_tested(table_tester_obj):
	methods_to_be_tested = [
		table_tester_obj.test_connect,
		table_tester_obj.test_yield_readable_timestamps,
		table_tester_obj.test_get_records,
		table_tester_obj.test_check_if_db_empty
		]
	return methods_to_be_tested


@pytest.mark.parametrize('table_tester_obj', [tt.TableTester(project_root, test_case_) for test_case_ in test_cases_exception_unable_to_open_database_file])
def test_exception_unable_to_open_database_file(table_tester_obj):
	methods_to_be_tested = get_methods_to_be_tested(table_tester_obj)
	for method_being_tested in methods_to_be_tested:
		try:
			method_being_tested()
		except sqlite3.OperationalError as excep:
			assert excep.args[0] == f'unable to open database file', (table_tester_obj, excep)
	
	return 'exception: no such table'

def run_tests_without_pytest():
	def test_exception_unable_to_open_database_file(table_tester_obj):
		methods_to_be_tested = get_methods_to_be_tested(table_tester_obj)
		if not methods_to_be_tested:
			raise ValueError('No methods specified for testing in get_methods_to_be_tested()')
		
		for method_being_tested in methods_to_be_tested:
			try:
				method_being_tested()
			except sqlite3.OperationalError as excep:
				assert excep.args[0] == f'unable to open database file', (table_tester_obj, excep)
		
		return 'exception: no such table'

	def test_Table_exception_unable_to_open_database_file():
		for table_arg_exception_ in test_cases_exception_unable_to_open_database_file:
			table_obj = tt.TableTester(project_root, table_arg_exception_)
			print('Passed:', test_exception_unable_to_open_database_file(table_obj))

	test_Table_exception_unable_to_open_database_file()

if __name__ == '__main__':
	run_tests_without_pytest()

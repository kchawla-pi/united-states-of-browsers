import pytest
import sqlite3

from pathlib import Path

from sqlite3 import OperationalError
from tests.nonpytest_test_table import table_tester as tt

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
                                       ]

@pytest.mark.parametrize('table_tester_obj', [tt.TableTester(project_root, test_case_) for test_case_ in test_cases_exception_no_such_table])
def test_exception_no_such_table(table_tester_obj):
	methods_to_be_tested = [
		table_tester_obj.test_connect,
		table_tester_obj.test_yield_readable_timestamps,
		table_tester_obj.test_get_records,
		table_tester_obj.test_check_if_db_empty
		]
	for method_being_tested in methods_to_be_tested:
		with pytest.raises(sqlite3.OperationalError):#(f'no such table: {table_tester_obj.test_data.table}')):
			method_being_tested()
	# 	except sqlite3.OperationalError as excep:
	# 		assert excep.args[0] == f'no such table: {table_tester_obj.test_data.table}'
	# return 'exception: no such table'


if __name__ == '__main__':
	def test_exception_no_such_table(table_tester_obj):
		methods_to_be_tested = [
			table_tester_obj.test_connect,
			table_tester_obj.test_yield_readable_timestamps,
			table_tester_obj.test_get_records,
			table_tester_obj.test_check_if_db_empty
			]
		for method_being_tested in methods_to_be_tested:
			try:
				method_being_tested()
			except sqlite3.OperationalError as excep:
				assert excep.args[0] == f'no such table: {table_tester_obj.test_data.table}'
		return 'exception: no such table'
	
	
	def test_Table_exceptions_no_such_table():
		for table_arg_exception_ in test_cases_exception_no_such_table:
			table_obj = tt.TableTester(project_root, table_arg_exception_)
			print('Passed:', test_exception_no_such_table(table_obj))
		
	test_Table_exceptions_no_such_table()

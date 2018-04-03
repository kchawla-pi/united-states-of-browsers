import sqlite3
from pathlib import Path

try:
	from . import test_table as tt
except ImportError:
	import test_table as tt

from tests.test_table.test_table_testcases import (test_cases_no_excep,
                                                   test_cases_exception_no_such_table,
                                                   test_cases_exception_unable_to_open_database_file,
                                                   )


def test_suite_no_exceptions(test_table_obj):
	test_results = [str(test_table_obj),
	                test_table_obj.test_connect(),
	                test_table_obj.test_yield_readable_timestamps(),
	                test_table_obj.test_get_records(),
	                test_table_obj.test_check_if_db_empty(),
	                ]
	return test_results


def test_exception_no_such_table(test_table_obj):
	methods_to_be_tested = [
		test_table_obj.test_connect,
		test_table_obj.test_yield_readable_timestamps,
		test_table_obj.test_get_records,
		test_table_obj.test_check_if_db_empty
		]
	for method_being_tested in methods_to_be_tested:
		try:
			method_being_tested()
		except sqlite3.OperationalError as excep:
			assert excep.args[0] == f'no such table: {test_table_obj.test_data.table}'
	return 'exception: no such table'


def test_exception_unable_to_open_database_file(test_table_obj):
	methods_to_be_tested = [
		test_table_obj.test_connect,
		test_table_obj.test_yield_readable_timestamps,
		test_table_obj.test_get_records,
		test_table_obj.test_check_if_db_empty
		]
	for method_being_tested in methods_to_be_tested:
		try:
			method_being_tested()
		except sqlite3.OperationalError as excep:
			assert excep.args[0] == f'unable to open database file', (test_table_obj, excep)
	
	return 'exception: no such table'


project_root = Path(__file__).parents[2]


def test_Table_no_exceptions():
	for table_arg_no_excep in test_cases_no_excep:
		table_no_excep = tt.TestTable(project_root, table_arg_no_excep)
		print('Passed:', test_suite_no_exceptions(table_no_excep))


def test_Table_exceptions_no_such_table():
	for table_arg_exception_ in test_cases_exception_no_such_table:
		table_obj = tt.TestTable(project_root, table_arg_exception_)
		print('Passed:', test_exception_no_such_table(table_obj))


def test_Table_exception_unable_to_open_database_file():
	for table_arg_exception_ in test_cases_exception_unable_to_open_database_file:
		table_obj = tt.TestTable(project_root, table_arg_exception_)
		print('Passed:', test_exception_unable_to_open_database_file(table_obj))
		
		
if __name__ == '__main__':
	test_Table_no_exceptions()
	test_Table_exceptions_no_such_table()
	# test_Table_exception_unable_to_open_database_file()

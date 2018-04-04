import sqlite3
from pathlib import Path
from tests.test_table import test_table as tt


project_root = Path(__file__).parents[2]

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


def test_Table_exception_unable_to_open_database_file():
	for table_arg_exception_ in test_cases_exception_unable_to_open_database_file:
		table_obj = tt.TestTable(project_root, table_arg_exception_)
		print('Passed:', test_exception_unable_to_open_database_file(table_obj))
		
		
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

if __name__ == '__main__':
	pass
	test_Table_exception_unable_to_open_database_file()

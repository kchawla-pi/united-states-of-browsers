import pytest
import sqlite3

from collections import namedtuple
from pathlib import Path

from united_states_of_browsers.db_merge.table import Table

project_root = Path(__file__).parents[2]

TableArgs = namedtuple('TableArgs', 'table path browser filename profile copies_subpath')
test_cases_exception_no_such_table = [
	TableArgs(table='moz_places',
	          path=Path(project_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Roaming/Mozilla/'
	                    'Firefox/Profiles/udd5sttq.test_profile2/moz_places.sqlite'),
	          browser='firefox',
	          filename='non_db_dummy_file_for_testing.txt',
	          profile='test_profile2',
	          copies_subpath=None,
	          ),
	TableArgs(table='urls',
	          path=Path(project_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Local/Google/Chrome/User Data/Profile 1/History_not_real'),
	          browser='chrome',
	          filename='History',
	          profile='Profile 1',
	          copies_subpath=None,
	          ),
	TableArgs(table='urls',
	          path=Path(project_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Local/Vivaldi/User Data/Default/History'),
	          browser='vivaldi',
	          filename='History',
	          profile='Default',
	          copies_subpath=None,
	          ),
	TableArgs(table='urls',
	          path=Path(project_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Roaming/Opera Software/Opera Stable/History'),
	          browser='opera',
	          filename='History',
	          profile='Opera Stable',
	          copies_subpath=None,
	          ),
	]


@pytest.mark.parametrize('test_case', [test_case for test_case in test_cases_exception_no_such_table])
def run_pytests(test_case):
	table_obj = Table(*test_case)
	with pytest.raises(sqlite3.DatabaseError) as excep:
		table_obj.get_records()


def run_non_pytests():
	for test_case in test_cases_exception_no_such_table:
		table_obj = Table(*test_case)
		table_obj.get_records()
		# try:
		# 	pass
		# except sqlite3.DatabaseError as excep:
		# 	print(excep, '--', test_case.browser, test_case.profile, test_case.filename, test_case.table)
		# else:
		# 	print('No error.', '--', test_case.browser, test_case.profile, test_case.filename, test_case.table)
		# finally:
		# 	print()
			# assert str(excep) == 'file is not a database'

if __name__ == '__main__':
	run_non_pytests()

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
	                    'tests/data/browser_profiles_for_testing_wrongpath_/AppData/Roaming/Mozilla/'
	                    'Firefox/Profiles/kceyj748.test_profile1/places.sqlite'),
	          browser='firefox',
	          filename='non_db_dummy_file_for_testing.txt',
	          profile='test_profile1',
	          copies_subpath=None,
	          ),
	TableArgs(table='urls',
	          path=Path(project_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Local/Google/Chrome/User Data/Profile 1 _wrongpath_/History'),
	          browser='chrome',
	          filename='History',
	          profile='Profile 1 _wrongpath_',
	          copies_subpath=None,
	          ),
	TableArgs(table='urls',
	          path=Path(project_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Local/Vivaldi/User_wrongpath_ Data/Default/History'),
	          browser='vivaldi',
	          filename='History',
	          profile='Default',
	          copies_subpath=None,
	          ),
	TableArgs(table='urls',
	          path=Path(project_root,
	                    'tests/data/browser_profiles_for_testing/AppData_wrongpath_/Roaming/Opera Software/Opera Stable/History'),
	          browser='opera',
	          filename='History',
	          profile='Opera Stable',
	          copies_subpath=None,
	          ),
	]


@pytest.mark.parametrize('test_case', [test_case for test_case in test_cases_exception_no_such_table])
def test_suite_os_error(test_case):
	table_obj = Table(*test_case)
	with pytest.raises(OSError) as excep:
		table_obj.get_records()


def non_pytest_test_suite_os_error():
	for test_case in test_cases_exception_no_such_table:
		table_obj = Table(*test_case)
		try:
			table_obj.get_records()
			pass
		except OSError as excep:
			print(f'Expected Exception raised', excep, '--', test_case.browser, test_case.profile, test_case.filename, test_case.table)
		except Exception as excep:
			raise excep
		else:
			print(f'Expected Exception NOT raised', '--', test_case.browser, test_case.profile, test_case.filename, test_case.table)
			raise Exception('Expected exception not raised.')
		finally:
			print()
		# break
			# assert str(excep) == 'file is not a database'

if __name__ == '__main__':
	non_pytest_test_suite_os_error()

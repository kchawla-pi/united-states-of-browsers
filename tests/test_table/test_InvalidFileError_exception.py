import pytest
from collections import namedtuple
from pathlib import Path

from united_states_of_browsers.db_merge.table import Table
from united_states_of_browsers.db_merge.custom_exceptions import InvalidFileError

project_root = Path(__file__).parents[2]

TableArgs = namedtuple('TableArgs', 'table path browser filename profile copies_subpath')
test_cases_exception_InvalidFileError = [
	TableArgs(table='moz_places',
	          path=Path(project_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Roaming/Mozilla/'
	                    'Firefox/Profiles/udd5sttq.test_profile2/non_db_dummy_file_for_testing.txt'),
	          browser='firefox',
	          filename='non_db_dummy_file_for_testing.txt',
	          profile='test_profile2',
	          copies_subpath=None,
	          ),
	TableArgs(table='moz_places',
	          path=Path(project_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Roaming/Mozilla/'
	                    'Firefox/Profiles/udd5sttq.test_profile2/places_non_existent.sqlite'),
	          browser='firefox',
	          filename='places_non_existent.sqlite',
	          profile='test_profile2',
	          copies_subpath=None,
	          ),
	TableArgs(table='urls',
	          path=Path(project_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Local/Google/Chrome/User Data/Profile 1/History_false_filename'),
	          browser='chrome',
	          filename='History_false_filename',
	          profile='Profile 1',
	          copies_subpath=None,
	          ),
	TableArgs(table='urls',
	          path=Path(project_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Local/Vivaldi/User Data/Default/History_false_filename'),
	          browser='vivaldi',
	          filename='History',
	          profile='Default',
	          copies_subpath=None,
	          ),
	TableArgs(table='urls',
	          path=Path(project_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Roaming/Opera Software/Opera Stable/History_false_filename'),
	          browser='opera',
	          filename='History',
	          profile='Opera Stable',
	          copies_subpath=None,
	          ),
	]


@pytest.mark.parametrize('test_case', [test_case for test_case in test_cases_exception_InvalidFileError])
def test_InvalidFileError(test_case):
	table_obj = Table(*test_case)
	with pytest.raises(InvalidFileError):
		table_obj.make_records_yielder()


def non_pytest_test_InvalidFileError(test_suite):
	for test_case in test_suite:
		table_obj = Table(*test_case)
		try:
			table_obj.make_records_yielder()
		except InvalidFileError as excep:
			print('Expected exception raised: InvalidFileError', excep, '--', test_case.browser, test_case.profile,
			      test_case.filename, test_case.table)
		else:
			print('Expected exception InvalidFileError NOT raised: .', '--', test_case.browser, test_case.profile,
			      test_case.filename, test_case.table)
			raise Exception
		finally:
			print()


def simply_run(test_suite):
	for test_case in test_suite:
		table_obj = Table(*test_case)
		table_obj.make_records_yielder()


if __name__ == '__main__':
	non_pytest_test_InvalidFileError(test_suite=test_cases_exception_InvalidFileError)
	quit()
	# simply_run(test_suite=test_cases_exception_InvalidFileError)
	fx_false_file = Table(table='moz_places',
	                      path=Path(project_root,
	                                'tests/data/browser_profiles_for_testing/AppData/Roaming/Mozilla/'
	                                'Firefox/Profiles/udd5sttq.test_profile2/non_db_dummy_file_for_testing.txt'),
	                      browser='firefox',
	                      filename='non_db_dummy_file_for_testing.txt',
	                      profile='test_profile2',
	                      copies_subpath=None,
	                      )

	# fx_false_file.make_records_yielder()

	chrome_false_file = Table(table='urls',
	                          path=Path(project_root,
	                                    'tests/data/browser_profiles_for_testing/AppData/Local/Google/Chrome/User Data/Profile 1/History_false_filename'),
	                          browser='chrome',
	                          filename='History_false_filename',
	                          profile='Profile 1',
	                          copies_subpath=None,
	                          )
	chrome_false_file.make_records_yielder()
	print(list(chrome_false_file.records_yielder))

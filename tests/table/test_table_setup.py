from collections import namedtuple

from united_states_of_browsers.project_path import get_project_root_path


def no_error_browser_info():
	firefox_info = {
		'browser': 'firefox',
		'pathcrumbs': ('Roaming', 'Mozilla', 'Firefox', 'Profiles'),
		'profiles': ('e0pj4lec.test_profile0', 'kceyj748.test_profile1',),
		'files_tables': {'places.sqlite': ('moz_places',),
		                 },
		}
	
	opera_info = {
		'browser': 'opera',
		'pathcrumbs': ('Roaming', 'Opera Software',),
		'profiles': ('Opera Stable',),
		'files_tables': {'History': ('urls',),
		                 },
		}
	
	chrome_info = {
		'browser': 'chrome',
		'pathcrumbs': ('Local', 'Google', 'Chrome', 'User Data'),
		'profiles': ('Profile 1',),
		'files_tables': {'history': ('urls',),
		                 },
		}
	
	vivaldi_info = {
		'browser': 'vivaldi',
		'pathcrumbs': ('Local', 'Vivaldi', 'User Data'),
		'profiles': ('Default',),
		'files_tables': {'History': ('urls',),
		                 },
		}
	return firefox_info, opera_info, chrome_info, vivaldi_info


def no_such_table_browser_info():
	firefox_info = {
		'browser': 'firefox',
		'pathcrumbs': ('Roaming', 'Mozilla', 'Firefox', 'Profiles'),
		'profiles': ('udd5sttq.test_profile2',),
		'files_tables': {'places.sqlite': ('moz_places',),
		                 },
		}
	return firefox_info


def yield_paths_tables(browsers, tests_root_path):
	for browser_ in browsers:
		for profile_ in browser_['profiles']:
			for file_ in browser_['files_tables']:
				path = tests_root_path.joinpath(*browser_['pathcrumbs'], profile_, file_)
				for table_ in browser_['files_tables'][file_]:
					yield TableArgs(
							table=table_, path=path, browser=browser_['browser'], filename=file_,
							profile=profile_, copies_subpath=None
							)


def no_error_test_setup():
	browsers = no_error_browser_info()
	path_table_yielder = yield_paths_tables(browsers, tests_root)
	return path_table_yielder

def no_such_table_test_setup():
	browsers = no_such_table_browser_info()
	path_table_yielder = yield_paths_tables(browsers, tests_root)
	return path_table_yielder


project_root = get_project_root_path('UnitedStatesOfBrowsers')
tests_root = project_root.joinpath('tests', 'data', 'browser_profiles_for_testing', 'AppData')
TableArgs = namedtuple('TableArgs', 'table path browser filename profile copies_subpath')

from collections import namedtuple

from united_states_of_browsers.oops.browser import Browser


def test_firefox():
	browser = 'firefox'
	profile_root = '~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles'

	profiles = ['test_profile0', 'test_profile1']

	file_tables={'places.sqlite': ['moz_places', 'moz_bookmarks'],
	             'permissions.sqlite': ['moz_hosts', 'moz_perms'],
	             }
	file_tables_list = list((file_tables.items()))

	def firefox_test_all_no_init_fn():
		print('\nfirefox_test_all_no_init')
		firefox_test_all_no_init = Browser(browser=browser, profile_root=profile_root)
		firefox_test_all_no_init.access_table(*file_tables_list[0])
		firefox_test_all_no_init.access_table(*file_tables_list[1])

	def firefox_test_some_no_init_fn():
		print('\nfirefox_test_some_no_init')
		firefox_test_some_no_init = Browser(browser, profile_root, profiles)
		firefox_test_some_no_init.access_table(*file_tables_list[0])
		firefox_test_some_no_init.access_table(*file_tables_list[1])

	def firefox_test_some_init_fn():
		print('\nfirefox_test_some_init')
		firefox_test_some_init = Browser(browser, profile_root, profiles, file_tables)

	def firefox_test_all_init_fn():
		print('\nfirefox_test_all_init')
		firefox_test_all_init = Browser(browser, profile_root, None, file_tables)

	def firefox_test_one_one_init_fn():
		print('\nfirefox_test_one_one_init')
		firefox_test_one_one_init = Browser(browser, profile_root, ['test_profile0'], {'places.sqlite': ['moz_places']})

	def firefox_test_glitched_profile():
		print('\nfirefox_test_one_one_init')
		firefox_test_one_one_init = Browser(browser, profile_root, ['test_profile2'], {'places.sqlite': ['moz_places']})

	firefox_test_all_no_init_fn()
	firefox_test_some_no_init_fn()
	firefox_test_some_init_fn()
	firefox_test_all_init_fn()
	firefox_test_one_one_init_fn()
	firefox_test_glitched_profile()


test_firefox()

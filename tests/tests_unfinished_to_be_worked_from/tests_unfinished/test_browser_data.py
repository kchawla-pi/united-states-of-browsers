
def test_browser():
	def fx_all():
		firefox_all = Browser(browser='firefox', profile_root='~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles')
		# firefox_all.make_paths()
		# pprint(firefox_all.paths)
		firefox_all.access_table('places.sqlite', ['moz_places', 'moz_bookmarks'])
		return firefox_all

	def fx_glitched():
		firefox_glitch = Browser(browser='firefox', profile_root='~\\AppData\\Roaming\\Mozilla\\Firefox_glitch\\Profiles')
		firefox_glitch.make_paths()
		return firefox_glitch

	# quit()
	def fx_some():
		profiles_list = ['test_profile0', 'test_profile1']
		firefox_some = Browser(browser='firefox',
		                            profile_root='~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles',
		                            profiles=profiles_list)
		firefox_some.make_paths()
		# pprint(firefox_some.paths)

		# pprint(firefox_some['tables'])

		firefox_some.access_table('places.sqlite', ['moz_places', 'moz_bookmarks'])
		# pprint(firefox_some['tables'])

		firefox_some.access_table('permissions.sqlite', ['moz_hosts', 'moz_perms'])
		# pprint(firefox_some['tables'])

		record_ids = [dict(record)['id'] for table in firefox_some.tables for record in table.records_yielder]
		# print(record_ids[::10])
		return firefox_some
		# pprint(firefox_some.tables)

	def chr():
		chrome = Browser(browser='chrome',
			                      profile_root='C:\\Users\\kshit\\AppData\\Local\\Google\\Chrome\\User Data')
		chrome.make_paths()
		chrome.access_table('history', ['urls'])
		record_ids = [dict(record)['id'] for table in chrome.tables for record in table.records_yielder]
		return chrome, record_ids[::10]

	def fx_auto():
		profiles_list = ['test_profile0', 'test_profile1']
		firefox_auto = Browser(browser='firefox',
		                       profile_root='~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles',
		                       profiles=profiles_list,
		                       file_tables={'places.sqlite': ['moz_places', 'moz_bookmarks'], 'permissions.sqlite': ['moz_hosts']})
		# pprint(firefox_auto.__dict__)
		return firefox_auto

	print('\n\tfx_auto()')
	fx_aut = fx_auto()
	# pprint(fx_aut)
	print(repr(fx_aut))


	print('\n\tfx_some()')
	fx_som = fx_some()
	# pprint(fx_som)
	print(repr(fx_som))
	# pprint(fx_som)
	print('***', fx_som)
	# pprint(fx_som.tables)

	# print('\n\tfx_all()')
	# fx_all()
	#
	# print('\n\tfx_glitched()')
	# fx_glitched()
	#
	print('\n\tchr()')
	chrm, ids = chr()
	print(repr(chrm))
	# objects_list = [firefox_all, firefox_some]
	# rb.print_objects(objects_list)
	# rb.print_objects([chrome])

def clean_test1():
	from pathlib import Path
	from pprint import pprint
	from united_states_of_browsers.oops.db_merge.browser import Browser
	
	browser = 'firefox'
	profile_root = Path('~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles').expanduser()
	print('profile_root', profile_root)
	profiles = ['test_profile0', 'test_profile1']
	
	file_tables = {'places.sqlite': ['moz_places', 'moz_bookmarks'],
	               'permissions.sqlite': ['moz_hosts', 'moz_perms'],
	               }
	
	# fx = Browser(browser, profile_root, profiles, {'places.sqlite': ['moz_places']})
	# fx.access_table('places.sqlite', ['moz_places'])
	# print(fx.tables)
	
	fx = Browser(browser, profile_root, profiles, file_tables)
	# pprint(fx.tables)
	records = fx.access_fields({'moz_places': ['id', 'url', 'title', 'last_visit_date']})
	for record_ in records:
		print(record_['table'], record_['profile'], record_['file'], record_['id'])
	print()
	
	records2 = fx.access_fields({'moz_bookmarks': ['id', 'title', 'dateAdded']})
	for record_ in records2:
		print(record_['table'], record_['profile'], record_['file'], record_['id'])
	
	print()
	cr = Browser(browser='chrome', profile_root='C:\\Users\\kshit\\AppData\\Local\\Google\\Chrome\\User Data',
	             profiles=None,
	             file_tables={'history': ['urls', 'meta']})
	records3 = cr.access_fields({'urls': ['id', 'url', 'title', 'last_visit_time']})
	for record_ in records3:
		print(record_['table'], record_['profile'], record_['file'], record_['id'])
	records4 = cr.access_fields({'meta': ['key', 'value']})
	for record_ in records4:
		print(record_['table'], record_['profile'], record_['file'], record_['key'], record_['value'])
	
	quit()
	print(fx.tables)
	print('\n' * 4)
	
	# fx.access_table('places.sqlite', ['moz_places'])
	# records = fx.access_fields({'moz_places': ['id', 'url', 'title', 'last_visit_date']})
	# pprint(list(records))
	
	quit()
	args = (browser, profile_root, ['test_profile2'], {'permissions.sqlite': ['moz_hosts', 'moz_perms']})
	pprint(Browser(*args[:]))
	firefox_test_all_init = Browser(browser, profile_root, None, file_tables)
	for entry in profile_root.iterdir():
		# print('*e', entry)
		for profile in profiles:
			if profile != 'test_profile0':
				print('*p', profile)
			if str(profile).lower() in str(entry).lower() and not entry.is_dir():
				pass
				print(entry)
				print(entry.stat())

# pprint(list(profile_root.iterdir()))


def clean_test2():
	from united_states_of_browsers.oops.db_merge.browser import Browser
	
	firefox = Browser(browser='firefox', profile_root='~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles',
	                  profiles=['profile0', 'profile1'],
	                  file_tables={'places.sqlite': ['moz_places', 'moz_bookmarks'], 'favicons.sqlite': ['moz_icons']}
	                  )
	
	# firefox.
	moz_places_accessor = firefox.access_fields({'moz_places': ['id', 'url', 'title', 'last_visit_date']})
	for rec in moz_places_accessor:
		print(rec['id'], rec['profile'], rec['table'])
	# input()
	print()
	moz_icons_accessor = firefox.access_fields({'moz_icons': ['id', 'icon_url', 'width']})
	for rec in moz_icons_accessor:
		print(rec['id'], rec['profile'], rec['table'])
	# input()
	
	# m_p = list(moz_places_accessor)
	# pprint(m_p[0:100])
	# print(firefox)
	# pprint(firefox['tables'])
	quit()
	
	table_fields = {
		'moz_places': ['id', 'url', 'title', 'last_visit_date'],
		'moz_icons': ['id', 'icon_url', 'width'],
		}
	firefox.combine_tables(table_fields)

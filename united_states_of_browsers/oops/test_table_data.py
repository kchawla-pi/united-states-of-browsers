from collections import namedtuple

from united_states_of_browsers.oops.table import Table

TableData = namedtuple('TableData','table, path, browser, file, profile')

firefox_profile_path = 'C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\'
init_testdata_input = (
	TableData(table='moz_places',
	          path=firefox_profile_path+'kceyj748.test_profile1\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='test_profile1',
	          ),
	TableData(table='moz_bookmarks',
	          path=firefox_profile_path+'kceyj748.test_profile1\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='test_profile1',
	          ),
	TableData(table='moz_places',
	          path=firefox_profile_path+'udd5sttq.test_profile2\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='test_profile2',
	          ),
	TableData(table='moz_places',
	          path=firefox_profile_path+'r057a01e.default\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='default',
	          ),
	)

init_testdata_expected = [
	Table(table='moz_places',
	          path=firefox_profile_path+'kceyj748.test_profile1\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='test_profile1',
	          ),
	Table(table='moz_bookmarks',
	          path=firefox_profile_path+'kceyj748.test_profile1\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='test_profile1',
	          ),
	Table(table='moz_places',
	          path=firefox_profile_path+'udd5sttq.test_profile2\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='test_profile2',
	          ),
	Table(table='moz_places',
	          path=firefox_profile_path+'r057a01e.default\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='default',
	          ),
	]

make_records_testdata_input = [
		Table(table='moz_places',
	          path=firefox_profile_path+'kceyj748.test_profile1\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='test_profile1',
	          ),
	]
make_records_testdata_expected = [
	'place:sort=8&maxResults=10',
	'place:type=6&sort=14&maxResults=10',
	'https://www.mozilla.org/privacy/firefox/',
	'https://www.nytimes.com/2017/10/20/opinion/sunday/to-complain-is-to-truly-be-alive.html',
	'https://www.wired.com/story/google-sidewalk-labs-toronto-quayside/',
	'https://www.outsideonline.com/2243621/appalachian-hustle',
	'place:type=3&sort=4',
	'place:transition=7&sort=4',
	'place:type=6&sort=1',
	'place:folder=TOOLBAR',
	'place:folder=BOOKMARKS_MENU',
	'place:folder=UNFILED_BOOKMARKS',
	]

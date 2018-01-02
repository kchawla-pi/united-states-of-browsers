from collections import namedtuple

from united_states_of_browsers.oops.table import Table

TableData = namedtuple('TableData','table, path, browser, file, profile')

firefox_profile_path = 'C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\'
table_testdata_input = (
	TableData(table='moz_places',
	          path=firefox_profile_path+'px2kvmlk.RegularSurfing\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='RegularSurfing',
	          ),
	TableData(table='moz_bookmarks',
	          path=firefox_profile_path+'px2kvmlk.RegularSurfing\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='default',
	          ),
	TableData(table='moz_places',
	          path=firefox_profile_path+'r057a01e.default\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='default',
	          ),
	TableData(table='moz_places',
	          path=firefox_profile_path+'r057a01e.default\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='default',
	          ),

	)
table_testdata_expected = [
	Table(table='moz_places',
	          path=firefox_profile_path+'px2kvmlk.RegularSurfing\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='RegularSurfing',
	          ),
	Table(table='moz_bookmarks',
	          path=firefox_profile_path+'px2kvmlk.RegularSurfing\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='default',
	          ),
	Table(table='moz_places',
	          path=firefox_profile_path+'r057a01e.default\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='default',
	          ),
	Table(table='moz_places',
	          path=firefox_profile_path+'r057a01e.default\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='default',
	          ),

	]

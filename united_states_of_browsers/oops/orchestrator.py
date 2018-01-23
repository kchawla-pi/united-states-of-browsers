import sqlite3

from united_states_of_browsers.oops.browser import Browser
from united_states_of_browsers.oops.helpers import make_queries


class Orchestrator:
	def make_records_yielders(self):
		firefox = Browser(browser='firefox', profile_root='~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles', profiles=None,
		                  file_tables={'places.sqlite': ['moz_places', 'moz_bookmarks'], 'favicons.sqlite': ['moz_icons']}
		                  )

		records_yielder_fx_moz_places = firefox.access_fields({'moz_places': ['id', 'url', 'title', 'last_visit_date']})
		# records_yielder_fx_moz_icons = firefox.access_fields({'moz_icons': ['id', 'icon_url', 'width']})
		chrome = Browser(browser='chrome', profile_root='~\\AppData\\Local\\Google\\Chrome\\User Data', profiles=None,
		                 file_tables={'history': ['urls']}
		                 )
		records_yielder_cr_urls = chrome.access_fields({'urls': ['id', 'url', 'title', 'last_visit_time']})

		opera = Browser(browser='opera', profile_root='~\\AppData\\Roaming\\Opera Software', profiles=['Opera Stable'],
		                file_tables={'History': ['urls']}
		                )
		records_yielder_op_urls = opera.access_fields({'urls': ['id', 'url', 'title', 'last_visit_time']})

		vivaldi = Browser(browser='vivaldi', profile_root='~\\AppData\\Local\\Vivaldi\\User Data', profiles=None,
		                  file_tables={'History': ['urls']}
		                  )
		records_yielder_viv = vivaldi.access_fields({'urls': ['id', 'url', 'title', 'last_visit_time']})

		self.records_yielders = (records_yielder_fx_moz_places, records_yielder_cr_urls, records_yielder_op_urls, records_yielder_viv)
		# self.records_yielders = (records_yielder_op_urls,)

	def write_records(self, tablename, fieldnames):
		queries = make_queries(tablename, fieldnames)

		with sqlite3.connect('combined_db_fx_cr.sqlite') as connection:
			cursor = connection.cursor()
			cursor.execute(queries['create'])
			[cursor.executemany(queries['insert'], browser_record_yielder) for browser_record_yielder in self.records_yielders]

	def orchestrate(self):
		self.make_records_yielders()
		fieldnames = ['id', 'url', 'title', 'last_visit_date', 'browser', 'profile', 'file', 'tablename']
		# using table as column name seems to conflict with SQL, table_ for example was not giving sqlite3 syntax error on create.
		self.write_records(tablename='history', fieldnames=fieldnames)


if __name__ == '__main__':
	write_combi_db = Orchestrator()
	write_combi_db.orchestrate()

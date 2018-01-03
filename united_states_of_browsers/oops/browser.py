import sqlite3

from collections import namedtuple
from pathlib import Path
from pprint import pprint

from united_states_of_browsers.oops.browserpaths import BrowserPaths
from united_states_of_browsers.oops.table import Table
from united_states_of_browsers.oops import recon_browsers as rb


TableMetadata = namedtuple('TableMetadata', 'browser profile file table')

class Browser:
	def __init__(self, browser, profile_root, profiles=None):
		self.browser = browser
		self.profile_root = profile_root
		self.files = None
		self.profiles = profiles
		self.paths = None
		self.table_yielders = []
		self.tables = []

	def make_paths(self):
		pathmaker = BrowserPaths(self.browser, self.profile_root)
		self.paths = pathmaker.profilepaths

	def make_table(self, file, tables):
		error_msg = set()
		current_batch = [Table(table, path.joinpath(file), self.browser, file, profile)
		                 for profile, path in self.paths.items()
		                 for table in tables
		                 ]
		for table in current_batch:
			try:
				table.get_records()
			except sqlite3.OperationalError as excep:
				if 'no such table' in str(excep) and table.check_if_db_empty():
					error_msg.add(f'Profile "{table.profile}" may not have any data.\nMoving on...')
				elif 'no such table' in str(excep) and table.check_if_db_empty():
					error_msg.add(f'Table {table.table} in database file {table.file} for profile {table.profile}.\n'
					              f'Verify the table and filename.\nMoving on...')
			else:
				self.tables.append(table)
		if error_msg:
			for msg in error_msg:
				print(msg)


	def get_table_yielders(self, tables):
		try:
			table_yielder = [Table(table, path, browser=self.browser, file=file, profile=profile)
			                 for (profile, file), path in self.paths.items()
			                 for table in tables
							 ]
		except Exception:
			raise
		else:
			self.tables.extend([TableMetadata(table_obj.browser, table_obj.profile, table_obj.file, table_obj.table)
			                    for table_obj in table_yielder
			                    ])
			self.table_yielders.append(table_yielder)


def test_browser():
	firefox_all = Browser(browser='firefox', profile_root='~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles')
	firefox_all.make_paths()
	# pprint(firefox_all.paths)
	firefox_all.make_table('places.sqlite', ['moz_places', 'moz_bookmarks'])


	quit()
	profiles_list = ['test_profile0', 'test_profile1']
	firefox_some = BrowserPaths(browser='firefox', files=files,
	                            profile_root='~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles',
	                            profiles=profiles_list)
	firefox_some.make_paths()

	chrome = BrowserPaths(browser='chrome', files=['history'],
	                      profile_root='C:\\Users\\kshit\\AppData\\Local\\Google\\Chrome\\User Data')

	objects_list = [firefox_all, firefox_some]
	# rb.print_objects(objects_list)
	# rb.print_objects([chrome])


if __name__ == '__main__':
	test_browser()
	# rb.get_tablenames('C:/Users/kshit/AppData/Roaming/Mozilla/Firefox/Profiles/vy2bqplf.dev-edition-default/places.sqlite')


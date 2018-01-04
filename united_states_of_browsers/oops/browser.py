import sqlite3

from collections import namedtuple
from pathlib import Path
from pprint import pprint

from united_states_of_browsers.oops.browserpaths import BrowserPaths
from united_states_of_browsers.oops.table import Table
from united_states_of_browsers.oops import recon_browsers as rb


TableMetadata = namedtuple('TableMetadata', 'browser profile file table')

class Browser(dict):
	""" Creates a generator of browser database records.
	Accepts parameters-
		browser: browser name
		profile_root: path to directory/folder where the browser stores all of its profiles
		profiles: list of profile, default is all profiles
		file_tables: dict of database file name containing the tables as keys, list of tables to be accessed as values.
	Methods-
		make_paths()
		make_table(file, tables)

	Usage-
		Using a single statement when creating a new Browser object.
			browser_obj = Browser(browser, profile_root, profiles, {database_file1: [table1, table2], database_file2: [table3, table4]})
		or
		Adding additional file and tables to existing Browser objects using the make_table() method.

			browser_obj = Browser(browser, profile_root, profiles)

			browser_obj.make_table(database_file1, [table1, table2])
			browser_obj.make_table(database_file2, [table3, table4])

		Access each table by iterating through browser_obj.tables, get each record by iterating through
		the records yielder for that table:
			for table in browser_obj.tables:
				for record in table.records_yielder:
					dict(record)
		or
		Use a comprehension to obtain all records across all tables in a file using a single statement:
			[dict(record) for table in browser_obj.tables for record in table.records_yielder]
	"""

	def __init__(self, browser, profile_root, profiles=None, file_tables=None):
		self.browser = browser
		self.profile_root = profile_root
		self.files = None
		self.profiles = profiles
		self.paths = None
		self.file_tables = file_tables
		self.tables = []
		self.make_paths()
		if self.file_tables:
			[self.make_table(file, tables) for file, tables in file_tables.items()]
		super().__init__(browser=self.browser, profile_root=self.profile_root, profiles=self.profiles,
		                 file_tables=self.file_tables, tables=self.tables)

	def make_paths(self):
		""" Creates the path to different browser profiles.
		"""
		pathmaker = BrowserPaths(self.browser, self.profile_root, self.profiles)
		self.paths = pathmaker.profilepaths

	def make_table(self, file, tables):
		""" Accepts name of file containing the tables and list of table names and creates corresponding Table objects.
		Accessed via the tables attribute.
		"""
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
					raise
			else:
				self.tables.append(table)
		if error_msg:
			for msg in error_msg:
				print(msg)


def test_browser():
	def fx_all():
		firefox_all = Browser(browser='firefox', profile_root='~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles')
		firefox_all.make_paths()
		# pprint(firefox_all.paths)
		firefox_all.make_table('places.sqlite', ['moz_places', 'moz_bookmarks'])
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
		pprint(firefox_some.paths)

		pprint(firefox_some['tables'])

		firefox_some.make_table('places.sqlite', ['moz_places', 'moz_bookmarks'])
		pprint(firefox_some['tables'])

		firefox_some.make_table('permissions.sqlite', ['moz_hosts', 'moz_perms'])
		pprint(firefox_some['tables'])

		record_ids = [dict(record)['id'] for table in firefox_some.tables for record in table.records_yielder]
		print(record_ids[::10])
		return firefox_some
		# pprint(firefox_some.tables)

	def chr():
		chrome = Browser(browser='chrome',
		                      profile_root='C:\\Users\\kshit\\AppData\\Local\\Google\\Chrome\\User Data')
		chrome.make_paths()
		chrome.make_table('history', ['urls'])
		record_ids = [dict(record)['id'] for table in chrome.tables for record in table.records_yielder]
		print(record_ids[::10])
		return chrome

	def fx_auto():
		profiles_list = ['test_profile0', 'test_profile1']
		firefox_auto = Browser(browser='firefox',
		                       profile_root='~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles',
		                       profiles=profiles_list,
		                       file_tables={'places.sqlite': ['moz_places', 'moz_bookmarks'], 'permissions.sqlite': ['moz_hosts']})
		# pprint(firefox_auto.__dict__)
		return firefox_auto

	print('\n\tfx_auto()')
	fx_auto()

	print('\n\tfx_some()')
	fx_some()

	# print('\n\tfx_all()')
	# fx_all()
	#
	# print('\n\tfx_glitched()')
	# fx_glitched()
	#
	# print('\n\tchr()')
	# chr()
	# objects_list = [firefox_all, firefox_some]
	# rb.print_objects(objects_list)
	# rb.print_objects([chrome])


if __name__ == '__main__':
	test_browser()
	# rb.get_tablenames('C:/Users/kshit/AppData/Roaming/Mozilla/Firefox/Profiles/vy2bqplf.dev-edition-default/places.sqlite')


from collections import namedtuple

from united_states_of_browsers.oops.browserpaths import BrowserPaths
from united_states_of_browsers.oops.tests.table import Table
from united_states_of_browsers.oops import exceptions_handling as exceph


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
		access_table(file, tables)

	Usage-
		Using a single statement when creating a new Browser object.
			browser_obj = Browser(browser, profile_root, profiles, {database_file1: [table1, table2], database_file2: [table3, table4]})
		or
		Adding additional file and tables to existing Browser objects using the access_table() method.

			browser_obj = Browser(browser, profile_root, profiles)
			browser_obj.access_table(database_file1, [table1, table2])
			browser_obj.access_table(database_file2, [table3, table4])

		Access each table by iterating through browser_obj.tables, get each record by iterating through
		the records yielder for that table:
			for table in browser_obj.tables:
				for record in table.records_yielder:
					dict(record)
		or
		Use a comprehension to obtain all records across all tables in a file using a single statement:
			[dict(record) for table in browser_obj.tables for record in table.records_yielder]
	"""

	def __init__(self, browser, profile_root, profiles=None, file_tables=None, not_null_fields=None, copies_subpath=None):
		self.browser = browser
		self.profile_root = profile_root
		self.profiles = profiles
		self.file_tables = file_tables
		self.not_null_fields = not_null_fields
		self.files = None
		self.paths = None
		self.tables = []
		self.copies_subpath = copies_subpath
		self.make_paths()
		if self.file_tables:
			self.error_msgs = []
			[self.access_table(file, tables) for file, tables in file_tables.items()]
			if self.error_msgs:
				self.error_msgs = exceph.exceptions_log_deduplicator(exceptions_log=self.error_msgs)
				print()
				for error_msg_ in self.error_msgs:
					try:
						print(f'{error_msg_.strerror}\n{error_msg_.filename}')
					except AttributeError as attr_err:
						print(error_msg_)
				print()
		super().__init__(browser=self.browser, profile_root=self.profile_root, profiles=self.profiles,
		                 file_tables=self.file_tables, tables=self.tables)

	def make_paths(self):
		""" Creates the path to different browser profiles.
		"""
		pathmaker = BrowserPaths(self.browser, self.profile_root, self.profiles)
		self.paths = pathmaker.profilepaths

	def access_table(self, file, tables, non_null_fields=None):
		""" Accepts name of file containing the tables and list of table names and creates corresponding Table objects.
		Accessed via the tables attribute.
		"""
		error_msg = []
		current_batch = [Table(table, path.joinpath(file), self.browser, file, profile, copies_subpath=self.copies_subpath)
		                 for profile, path in self.paths.items()
		                 for table in tables
		                 ]
		for table in current_batch:
			exception_raised = table.get_records()
			if exception_raised:
				error_msg.append(exception_raised)
			else:
				self.tables.append(table)
				try:
					self.profiles.add(table.profile)
				except AttributeError:
					self.profiles = set()
					self.profiles.add(table.profile)
		try:
			self.error_msgs.extend(error_msg)
		except AttributeError:
			if error_msg:
				error_msg = exceph.exceptions_log_deduplicator(error_msg)
				print()
				for error_msg_ in error_msg:
					try:
						print(f'{error_msg_.strerror}\n{error_msg_.filename}')
					except AttributeError as at_err:
						print(error_msg_)

	def access_fields(self, table_fields):
		additional_fields = ('browser', 'profile', 'file', 'table')
		current_table_across_profiles = [table for current_tablename in table_fields
		                                 for table in self.tables
		                                 if table.table == current_tablename
		                                 ]
		for current_table in current_table_across_profiles:
			fields = table_fields[current_table.table]
			selected_fields_records = dict.fromkeys(fields, None)
			selected_fields_records.update({field: current_table[field] for field in additional_fields})
			for record in current_table.records_yielder:
				selected_fields_records.update({field_: record[field_] for field_ in fields})
				# self.selected_fields_records = selected_fields_records
				yield tuple(selected_fields_records.values())
			current_table.get_records()


	def __repr__(self):
		return f'Browser("{self.browser}", "{self.profile_root}", {self.profiles}, {self.file_tables})'

	def __str__(self):
		return f'Browser: {self.browser}, files: {self.files}, profiles: {self.profiles}'

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


if __name__ == '__main__':
	# test_browser()
	# chrome = Browser(browser='chrome', profile_root='C:\\Users\\kshit\\AppData\\Local\\Google\\Chrome\\User Data')

	firefox_auto = Browser(browser='firefox',
	                       profile_root='~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles',
	                       profiles=['test_profile2'],
	                       file_tables={'places.sqlite': ['moz_places', 'moz_bookmarks'],
	                                    'permissions.sqlite': ['moz_hosts']})
	quit()
	firefox_auto = Browser(browser='firefox',
	                       profile_root='~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles',
	                       profiles=['test_profile0', 'test_profile1'],
	                       file_tables={'places.sqlite': ['moz_places', 'moz_bookmarks'],
	                                    'permissions.sqlite': ['moz_hosts']})

# rb.get_tablenames('C:/Users/kshit/AppData/Roaming/Mozilla/Firefox/Profiles/vy2bqplf.dev-edition-default/places.sqlite')


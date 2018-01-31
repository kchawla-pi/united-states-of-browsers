from collections import namedtuple

from united_states_of_browsers.db_merge.browserpaths import BrowserPaths
from united_states_of_browsers.db_merge.table import Table
from united_states_of_browsers.db_merge import exceptions_handling as exceph

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

	def __init__(self, browser, profile_root, profiles=None, file_tables=None, copies_subpath=None):
		self.browser = browser
		self.profile_root = profile_root
		self.profiles = profiles
		self.file_tables = file_tables
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


if __name__ == '__main__':
	# test_browser()
	# chrome = Browser(browser='chrome', profile_root='C:\\Users\\kshit\\AppData\\Local\\Google\\Chrome\\User Data')

	firefox_auto = Browser(browser='firefox',
	                       profile_root='~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles',
	                       profiles=['Employment'],
	                       file_tables={'places.sqlite': ['moz_places', 'moz_bookmarks'],
	                                    'permissions.sqlite': ['moz_hosts']})
	firefox_auto.access_fields({'moz_places': ['id', 'url', 'title', 'last_visit_date', 'last_visit_readable']})
	quit()
	firefox_auto = Browser(browser='firefox',
	                       profile_root='~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles',
	                       profiles=['test_profile0', 'test_profile1'],
	                       file_tables={'places.sqlite': ['moz_places', 'moz_bookmarks'],
	                                    'permissions.sqlite': ['moz_hosts']})

# rb.get_tablenames('C:/Users/kshit/AppData/Roaming/Mozilla/Firefox/Profiles/vy2bqplf.dev-edition-default/places.sqlite')


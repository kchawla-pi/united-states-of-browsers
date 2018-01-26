# -*- encoding: utf-8 -*-

import errno
import shutil
import sqlite3

from pathlib import Path

from united_states_of_browsers.oops import exceptions_handling as exceph
from united_states_of_browsers.oops.helpers import define_non_null_fields

class Table(dict):
	def __init__(self, table, path, browser, file, profile):
		super().__init__(table=table, path=path, browser=browser, file=file, profile=profile, non_null_fields=None)
		self.table = table
		self.path = Path(path)
		self.orig_path = Path(path)
		self.browser = browser
		self.file = file
		self.profile = profile
		self.records_yielder = None
		self._connection = None
		self.non_null_fields = define_non_null_fields(self)
		self.update(non_null_fields=self.non_null_fields)

	def _connect(self):
		""" Creates TableObject.connection to the database file specified in TableObject.path.
		Returns Exception on error.
		"""

		connection_arg = f'file:{self.path}?mode=ro'
		files_pre_connection_attempt = set(entry for entry in self.path.parents[1].iterdir() if entry.is_file())
		try:
			with sqlite3.connect(connection_arg, uri=True) as self._connection:
				self._connection.row_factory = sqlite3.Row
		except sqlite3.OperationalError as excep:
			if 'database is locked' in str(excep).lower():
				print('database is locked', '\n', str(self.path))
				raise excep
			elif 'unable to open database file' in str(excep).lower():
				invalid_path = exceph.invalid_path_in_tree(self.path)
				if invalid_path:
					return OSError(f'Path does not exist: {invalid_path}')
				elif not self.path.is_file():
					return OSError(errno.ENOENT, f'"{self.path.name}" is not a file, or the file does not exist. The profile "{self.profile}" might not contain any data.', str(self.path))#excep, f'{self.path.name} is not a file, or the file does not exist. The profile might not contain any data. ({self.path})')
				else:
					raise
			else:
				raise
		finally:
			# Cleans up any database files created uring failed connection attempt.
			exceph.remove_new_empty_files(dirpath=self.path.parents[1], existing_files=files_pre_connection_attempt)

	def _make_records_yielder(self):
		""" Yields a generator of all fields in TableObj.table
		"""
		cursor = self._connection.cursor()
		non_null_fields = define_non_null_fields(self)
		if non_null_fields:
			self.non_null_fields = non_null_fields
			not_null_query_string = ' OR '.join([f'{field_} IS NOT NULL' for field_ in self.non_null_fields])
			query = f'SELECT * FROM {self.table} WHERE {not_null_query_string}'
		else:
			query = f'SELECT * FROM {self.table}'
		records_yielder = cursor.execute(query)
		self.records_yielder = (dict(record) for record in records_yielder)

	def _create_db_copy(self):
		dst = Path('~', 'USB', 'AppData', 'Profile Copies', self.browser, self.profile).expanduser()
		dst.mkdir(parents=True,exist_ok=True)
		try:
			self.path = Path(shutil.copy2(self.path, dst))
		except FileNotFoundError as excep:
			return FileNotFoundError(errno.ENOENT, f'File {self.path.name} does not exist for {self.browser} profile "{self.profile}". The profile may be empty.', str(self.path))
		except shutil.SameFileError as excep:
			self.path = dst.joinpath(self.path.name)

	def get_records(self):
		""" Yields a generator to all fields in TableObj.table.
		"""
		file_copy_exception_raised = self._create_db_copy()
		if file_copy_exception_raised:
			return file_copy_exception_raised
		db_connect_exception_raised = self._connect()
		if db_connect_exception_raised:
			return db_connect_exception_raised
		else:
			try:
				self._make_records_yielder()
			except sqlite3.OperationalError as excep:
				if 'no such table' in str(excep):
					return ValueError(f'Table "{self.table}" does not exist in database file "{self.file}" in {self.browser} profile "{self.profile}". The profile may be empty.')
				return None

	def check_if_db_empty(self):
		cursor = self._connection.cursor()
		query = f'SELECT name FROM sqlite_master WHERE type = "table"'
		query_results = cursor.execute(query).fetchall()
		all_tables = [tuple(result_)[0] for result_ in query_results]
		return False if all_tables else True


def test_table():
	table = Table('1', '2', '3', '4', '5')


def test_firefox():
	table2 = Table(table='moz_places',
	               path=Path('C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\px2kvmlk.RegularSurfing_glitch\\places.sqlite'),
	               browser='firefox',
	               file='places.sqlite',
	               profile='RegularSurfing',
	               )
	table2.get_records()
	# for record_yielder in table2.records_yielder:
	# 	pass
		# print(dict(record_yielder))

	table3 = Table(table='moz_places',
	               path='C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\e0pj4lec.test_profile0\\places.sqlite',
	               browser='firefox',
	               file='places.sqlite',
	               profile='test_profile0',
	               )
	table3.get_records()
	for record_yielder in table3.records_yielder:
		pass
		# print(dict(record_yielder))

	table4 = Table(table='moz_places',
	               path='C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\udd5sttq.test_profile2\\places.sqlite',
	               browser='firefox',
	               file='places.sqlite',
	               profile='test_profile0',
	               )
	# table4.get_records()
	# for record_yielder in table4.records_yielder:
	# 	pass
	# 	print(dict(record_yielder))

	table5 = Table(table='moz_places',
	               path='C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\kceyj748.test_profile1\\places.sqlite',
	               browser='firefox',
	               file='places.sqlite',
	               profile='test_profile0',
	               )
	table5.get_records()
	for record_yielder in table5.records_yielder:
		pass
		# print(dict(record_yielder)['url'])

def test_chrome():
	table2 = Table(table='urls',
	               path='C:\\Users\\kshit\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\history',
	               browser='chrome',
	               file='history',
	               profile='Default',
	               )
	not_null_fieldnames = define_non_null_fields(table2)

	table2.get_records()
	for record_yielder in table2.records_yielder:
		print(dict(record_yielder))

def test_define_non_null_fields():
	table_fx = Table(table='moz_places',
	               path='C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\udd5sttq.test_profile2\\places.sqlite',
	               browser='firefox',
	               file='places.sqlite',
	               profile='test_profile0',
	               )
	not_null_fieldnames = define_non_null_fields(table_fx)
	print(not_null_fieldnames, table_fx['non_null_fields'], table_fx.non_null_fields)
	table_cr = Table(table='urls',
	               path='C:\\Users\\kshit\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\history',
	               browser='chrome',
	               file='history',
	               profile='Default',
	               )
	not_null_fieldnames = define_non_null_fields(table_cr)
	print(not_null_fieldnames, table_cr['non_null_fields'], table_cr.non_null_fields)


def print_table_attr(obj):
	attrs = ('table', 'path', 'browser', 'file', 'profile')
	print([obj[attr_] for attr_ in attrs])
	print(obj)
	print('__str__:', repr(obj))
	print('__repr__:', obj.table)


def test():
	test_table()
	test_firefox()
	test_chrome()
	test_define_non_null_fields()


if __name__ == '__main__':
	table4 = Table(table='moz_places',
	               path='C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\udd5sttq.test_profile2\\places.sqlite',
	               browser='firefox',
	               file='places.sqlite',
	               profile='test_profile0',
	               )

	# test()

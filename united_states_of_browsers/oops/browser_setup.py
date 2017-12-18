# -*- encoding: utf-8 -*-
"""
Object Oriented version of browser_setup.py . Ease of handling for multiple browsers.
"""
import contextlib
import shutil
import sys
import sqlite3
import tempfile

from pathlib import Path
from pprint import pprint

from united_states_of_browsers.db_merge.imported_annotations import *

raise_exceps = 0


class TemporaryCopy:
	def __init__(self, original_file):
		self.original_file = Path(original_file)
		self.temp_db = None

	def __enter__(self):
		filename = Path(self.original_file).name
		tempdir = Path(__file__).parents[1].joinpath('appdata', 'temp')
		tempfile.mkdtemp(tempdir)
		self.temp_db = tempdir.joinpath(filename)
		shutil.copy2(self.original_file, self.temp_db)
		yield self.temp_db

	def __exit__(self):
		shutil.rmtree(self.temp_db)



class Browser(dict):
	def __init__(self, browser, profile_pathcrumbs: Union[Iterable[AnyStr], PathInfo], database_files: Iterable[Text]):
		""" Accepts the browser name and/or a dict of pathrcrumbs for it.
		Figures out the current platform and chooses pathcrumbs accordingly.
		"""
		self.browser = browser
		self.pathcrumbs = profile_pathcrumbs
		self.files = database_files
		self.os = sys.platform
		self.db_info = None
		self.tables = dict()

	#
	def __getitem__(self, item):
		return self.__dict__[item]

	def keys(self):
		return self.__dict__.keys()

	def setup_paths(self) -> Iterable[Dict[Tuple[Text, Text], PathInfo]]:
		profile_root = Path(*self.pathcrumbs).expanduser()
		try:
			profile_paths = {profile.name.split(sep='.', maxsplit=1)[1]: profile for profile in profile_root.iterdir()}
		except IndexError:
			profile_paths = {profile.name: profile for profile in profile_root.iterdir() if
			                 profile.name.startswith('Profile') or profile.name == 'Default'}
		self.db_info = [{'browser': self.browser, 'profile': profile, 'file': file, 'path': path.joinpath(file)} for
		                profile, path in profile_paths.items() for file in self.files]

	def _connect(self, path) -> Generator:
		connection_arg = f'file:{path}?mode=ro'
		try:
			with sqlite3.connect(connection_arg, uri=True) as connection:
				connection.row_factory = sqlite3.Row
				return connection.cursor()
		except sqlite3.OperationalError as excep:
			if 'database is locked' in str(excep).lower():
				print('retrying...')  ##
				with TemporaryCopy(path) as temp_db:
					return self._connect(temp_db)

	def _get_table_info(self, cursor):
		query = 'SELECT * FROM sqlite_master;'
		query_result = cursor.execute(query)
		return [dict(table_entry) for table_entry in query_result]

	# self.table.update({'browser': self.browser, 'file': file})

	def read_table_info_buggy(self):
		db_info_copy = self.db_info.copy()
		for idx, entry in enumerate(db_info_copy):
			profile, file, path = entry['profile'], entry['file'], entry['path']
			cursor = self._connect(path)
			try:
				tables = self._get_table_info(cursor)
				print(tables)
			except sqlite3.OperationalError as excep:
				if not path.exists():
					if raise_exceps:
						raise FileNotFoundError(str(path))
					else:
						print(f'\nFAILED: Browser._connect().\n'
						      f'Connecting to {path} failed.\n'
						      f'File {file} does not exist for {profile}.\n'
						      f'Removing erring entries and moving on...\n'
						      )
						self.db_info.pop(idx)
				else:
					raise sqlite3.OperationalError(excep)
			else:
				entry.update({'tables': tables})
		pass

	def read_table_info(self):
		print('read_table_info')
		# print(self.db_info)


class DBFile:
	def __init__(self, dbpath):
		self.dbpath = dbpath
		self.filename = dbpath.name
		self.connection = None
		self.tables_info = None
		self.tables = None
		self.tablenames = None

		self.Table = Table

	def _connect(self):
		with sqlite3.connect(str(self.dbpath)) as conn:
			conn.row_factory = sqlite3.Row
			self.connection = conn

	def _tables_info(self):
		query = 'SELECT * FROM sqlite_master'
		cur = self.connection.cursor()
		result = cur.execute(query)
		self.tables_info = [dict(entry) for entry in result]
		self.tablenames = [table_['name'] for table_ in self.tables_info]

	def _tables_fields(self):
		query = 'SELECT * FROM moz_places'
		cur = self.connection.cursor()
		result = cur.execute(query)
		table = [dict(entry) for entry in result]
		return table

	def read_tables(self):
		self.tables = [self.Table(table_, self.connection) for table_ in self.tablenames]

		# for table in self.Table


class Table(object):
	def __init__(self, tablename, connection):
		# super().__init__(tablename=tablename, connection=connection)
		self.tablename = tablename
		self.fieldnames = None
		self.record_yielder = None
		self.connection = connection
		table_data = None

	def get_fieldnames(self):
		# query = 'SELECT * from (?)'
		cur = self.connection.cursor()
		fieldnames = cur.desc
		self.fieldnames = fieldnames

	def yield_record(self):
		query = 'SELECT * from (?)'
		cur = self.connection.cursor()
		result = cur.execute(query, self.tablename)
		self.record_yielder = (dict(record) for record in result)

	def __iter__(self):
		query = 'SELECT * from (?)'
		cur = self.connection.cursor()
		self.record_yielder = cur.execute(query, self.tablename)
		return self

	def __next__(self):
		# next(self.record_yielder, None)
		yield from self.record_yielder

	def __str__(self):
		return f'\{tablename: {self.tablename}, fieldnames: {self.fieldnames}\}'

	def __repr__(self):
		return f'Table({self.tablename})'



def test_firefox():
	profile_pathcrumbs_firefox = ['~', 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles']
	firefox = Browser('firefox', profile_pathcrumbs_firefox, ['places.sqlite', 'favicons.sqlite', 'arbit'])
	firefox.setup_paths()
	print((firefox.db_info[0])['path'])

	one_file = DBFile((firefox.db_info[0])['path'])
	one_file._connect()
	one_file._tables_info()
	# print(one_file.tablenames)


	# Table((one_file.tablenames[0])

	one_file.read_tables()
	# pprint(one_file.tables)
	# print(one_file.tables[0])
	# print([dict(record) for record in one_file.tables[0].record_yielder])

def test_Table(path):
	with sqlite3.connect(path) as connection:
		table = Table('moz_places', connection)
		print(table)

def other():
	profile_pathcrumbs_firefox = ['~', 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles']
	chrome_path = f'~\\AppData\\Local\\Google\\Chrome\\User Data\\Default'
	chrome_path = f'~\\AppData\\Local\\Google\\Chrome\\User Data'

	firefox = Browser('firefox', profile_pathcrumbs_firefox, ['places.sqlite', 'favicons.sqlite', 'arbit'])
	firefox.setup_paths()

	print((firefox.db_info[0])['path'])
	one_file = DBFile((firefox.db_info[0])['path'])
	one_file._connect()
	one_file._tables_info()
	pprint(one_file.tablenames)
	# pprint(one_file.tables_info)
	# pprint(one_file._tables_fields())

	# one_profile_cur = one_file._connect()
	# query_result = one_profile_cur.execute('SELECT * FROM sqlite_master')
	# query_ans = [dict(entry) for entry in query_result]
	# print(query_ans)
	# pprint(firefox.db_info)


	# firefox.read_table_info()
	# chrome = Browser('chrome', [chrome_path], ['history_copy'])
	# print(chrome)
	# chrome.setup_paths()
	# chrome.read_table_info()
	# pprint(chrome['db_info'])

	# print(firefox['browser'])
	# print(firefox['pathcrumbs'])
	# print(firefox['browser'])
	# print(firefox.__dict__.keys())

	# temp_path = db_paths[('test_profile0', 'arbit')]; temp_conn = f'file:{temp_path}?mode=ro'; temp_gen = self._connect(temp_path); print(next(temp_gen, None))
if __name__ == '__main__':
	test_firefox()

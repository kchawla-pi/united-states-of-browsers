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





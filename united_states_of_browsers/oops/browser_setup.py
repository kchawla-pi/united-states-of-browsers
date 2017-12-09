# -*- encoding: utf-8 -*-
"""
Object Oriented version of browser_setup.py . Ease of handling for multiple browsers.
"""
import sys
import sqlite3

from pathlib import Path
from pprint import pprint

from united_states_of_browsers.db_merge.imported_annotations import *

raise_exceps = 0

class Browser(dict):
	def __init__(self, browser, profile_pathcrumbs: Union[Iterable[AnyStr], PathInfo], database_files:Iterable[Text]):
		""" Accepts the browser name and/or a dict of pathrcrumbs for it.
		Figures out the current platform and chooses pathcrumbs accordingly.
		"""
		self.browser = browser
		self.pathcrumbs = profile_pathcrumbs
		self.files = database_files
		self.os = sys.platform
		self.db_info = None
		self.connection = None
		self.cursor = None
		self.tables = {}
	#
	def __getitem__(self, item):
		return self.__dict__[item]

	def keys(self):
		return self.__dict__.keys()

	def setup_paths(self) -> Iterable[Dict[Tuple[Text, Text], PathInfo]]:
		profile_root = Path(*self.pathcrumbs).expanduser()
		profile_paths = {profile.name.split(sep='.', maxsplit=1)[1]: profile for profile in profile_root.iterdir()}
		self.db_info = [{'browser': self.browser, 'profile': profile, 'file': file, 'path': path.joinpath(file)} for profile, path in profile_paths.items() for file in self.files]
		# return db_paths

	def _connect(self, path) -> Generator:
		connection_arg = f'file:{path}?mode=ro'
		with sqlite3.connect(connection_arg, uri=True) as connection:
			connection.row_factory = sqlite3.Row
			return connection.cursor()


	def _get_table_info(self, cursor):
		query = 'SELECT * FROM sqlite_master;'
		cursor.execute(query)
		return [dict(table_entry) for table_entry in cursor]

		# self.table.update({'browser': self.browser, 'file': file})

	def read_table_info(self):
		for idx, entry in enumerate(self.db_info):
			profile, file, path = entry['profile'], entry['file'], entry['path']
			try:
				cursor = self._connect(path)
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
				tables = self._get_table_info(cursor)
				entry.update({'tables': tables})
		pass

if __name__ == '__main__':
	profile_pathcrumbs_firefox = ['~', 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles']
	chrome_path = f'~\\AppData\\Local\\Google\\Chrome\\User Data\\Default'
	chrome_path = f'~\\AppData\\Local\\Google\\Chrome\\User Data'

	firefox = Browser('firefox', profile_pathcrumbs_firefox, ['places.sqlite', 'favicons.sqlite', 'arbit'])
	firefox.setup_paths()
	# pprint(firefox.db_info)
	firefox.read_table_info()
	chrome = Browser('chrome', [chrome_path], ['history'])
	print(chrome)
	# chrome.setup_paths()
	# print(firefox['browser'])
	# print(firefox['pathcrumbs'])
	# print(firefox['browser'])
	# print(firefox.__dict__.keys())

# temp_path = db_paths[('test_profile0', 'arbit')]; temp_conn = f'file:{temp_path}?mode=ro'; temp_gen = self._connect(temp_path); print(next(temp_gen, None))

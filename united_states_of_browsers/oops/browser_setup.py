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

class Browser:
	def __init__(self, profile_pathcrumbs: Union[Iterable[AnyStr], PathInfo], database_files:Iterable[Text]):
		""" Accepts the browser name and/or a dict of pathrcrumbs for it.
		Figures out the current platform and chooses pathcrumbs accordingly.
		"""
		self.pathcrumbs = profile_pathcrumbs
		self.files = database_files
		self.os = sys.platform
		self.db_paths = None
		self.cursor = None

	def setup_paths(self) -> Iterable[Dict[Tuple[Text, Text], PathInfo]]:
		profile_root = Path(*self.pathcrumbs).expanduser()
		profile_paths = {profile.name.split(sep='.', maxsplit=1)[1]: profile for profile in profile_root.iterdir()}
		self.db_paths = {(profile, file): path.joinpath(file) for profile, path in profile_paths.items() for file in self.files}
		# return db_paths

	def _connect(self, path) -> Generator:
		connection_arg = f'file:{path}?mode=ro'
		with sqlite3.connect(connection_arg, uri=True) as connection:
			connection.row_factory = sqlite3.Row
			cursor = connection.cursor()
			return cursor

	def _get_table_info(self, cursor):
		query = 'SELECT * FROM sqlite_master;'
		cursor.execute(query)
		return cursor

	def read_table(self):
		for (profile, file), path in self.db_paths.items():
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
						      f'Moving on...\n'
						      )
				else:
					raise sqlite3.OperationalError(excep)
			else:
				table_info = self._get_table_info(cursor)
				pprint(table_info.fetchone())
		pass

if __name__ == '__main__':
	browser_info = profile_pathcrumbs_firefox = ['~', 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles']
	chrome_path = f'~\\AppData\\Local\\Google\\Chrome\\User Data\\Default'

	firefox = Browser(profile_pathcrumbs_firefox, ['places.sqlite', 'favicons.sqlite', 'arbit'])
	firefox.setup_paths()
	firefox.read_table()

# temp_path = db_paths[('test_profile0', 'arbit')]; temp_conn = f'file:{temp_path}?mode=ro'; temp_gen = self._connect(temp_path); print(next(temp_gen, None))

# -*- encoding: utf-8 -*-
"""
Object Oriented version of browser_setup.py . Ease of handling for multiple browsers.
"""
import sys
import sqlite3

from pathlib import Path
from pprint import pprint

from united_states_of_browsers.db_merge.imported_annotations import *


class Browser:
	def __init__(self, profile_pathcrumbs: Union[Iterable[AnyStr], PathInfo], database_files:Iterable[Text]):
		""" Accepts the browser name and/or a dict of pathrcrumbs for it.
		Figures out the current platform and chooses pathcrumbs accordingly.
		"""
		self.pathcrumbs = profile_pathcrumbs
		self.files = database_files
		self.os = sys.platform
		self.db_paths = self.setup_paths()

	def setup_paths(self) -> Iterable[Dict[Tuple[Text, Text], PathInfo]]:
		profile_root = Path(*self.pathcrumbs).expanduser()
		profile_paths = {profile.name.split(sep='.', maxsplit=1)[1]: profile for profile in profile_root.iterdir()}
		db_paths = {(profile, file): path.joinpath(file) for profile, path in profile_paths.items() for file in self.files}
		return db_paths

	def _connect(self, database: Dict[Tuple[Text, Text], PathInfo]) -> Generator:
		(profile, file), path = tuple(*database.items())
		connection_arg = f'file:{database}?mode=ro'
		try:
			with sqlite3.connect(connection_arg, uri=True) as connection:
				cursor = connection.cursor()
				yield cursor
		except sqlite3.OperationalError as excep:
			if not database.exists():
				# raise FileNotFoundError(str(database))
				print(f'FAILED: Browser._connect().\nConnecting to {database} failed.\nFile does not exist.\nMoving on...')
			else:
				raise sqlite3.OperationalError(excep)

	def get_table_info(self):
		pass

	def read_table(self):
		pass

if __name__ == '__main__':
	browser_info = profile_pathcrumbs_firefox = ['~', 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles']
	chrome_path = f'~\\AppData\\Local\\Google\\Chrome\\User Data\\Default'

	firefox = Browser(profile_pathcrumbs_firefox, ['places.sqlite', 'favicons.sqlite', 'arbit'])

# temp_path = db_paths[('test_profile0', 'arbit')]; temp_conn = f'file:{temp_path}?mode=ro'; temp_gen = self._connect(temp_path); print(next(temp_gen, None))

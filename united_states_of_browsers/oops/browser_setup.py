# -*- encoding: utf-8 -*-
"""
Object Oriented version of browser_setup.py . Ease of handling for multiple browsers.
"""
import sys

from pathlib import Path


class Browser:
	def __init__(self, profile_pathcrumbs, database_files):
		""" Accepts the browser name and/or a dict of pathrcrumbs for it.
		Figures out the current platform and chooses pathcrumbs accordingly.
		"""
		self.pathcrumbs = profile_pathcrumbs
		self.files = database_files
		self.os = sys.platform
		self.db_paths = self.setup_paths()

	def setup_paths(self):
		profile_root = Path(*self.pathcrumbs).expanduser()
		profile_paths = {profile.name.split(sep='.', maxsplit=1)[1]: profile for profile in profile_root.iterdir()}
		# db_paths = for file in self.files

	def get_table_info(self):
		pass

	def read_table(self):
		pass

if __name__ == '__main__':
	browser_info = profile_pathcrumbs_firefox = ['~', 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles']
	chrome_path = f'~\\AppData\\Local\\Google\\Chrome\\User Data\\Default'

	firefox = Browser(profile_pathcrumbs_firefox, ['places.sqlite', 'favicons.sqlite'])

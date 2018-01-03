# -*- encoding: utf-8 -*-
"""
Module containing classes to setup browser profile and dtaabase file paths.

Classes: BrowserPaths
"""
from pathlib import Path
from pprint import pprint


class BrowserPaths(dict):
	"""	Creates objects to create paths to browser profile and database files.
	Accepts browser name, browser profiles directory path, database files list, browser profiles list (default: all).

	"""
	def __init__(self, browser, files, profile_root, profiles=None):
		self.browser = browser
		self.profile_root = Path(profile_root).expanduser()
		self.profiles = profiles
		self.files = files
		self.profilepaths = None
		self.filepaths = None
		self.make_paths()
		super().__init__(browser=browser, profile_root=self.profile_root, profiles=profiles, profilepaths=self.profilepaths,
		                 files=files, filepaths=self.filepaths
		                 )

	def _make_profile_paths(self):
		if self.profiles:
			self.profilepaths = {str(entry).split('.', maxsplit=1)[1]: entry for entry in self.profile_root.iterdir()
			                     for profile in self.profiles
			                     if str(profile).lower() in str(entry).lower()
			                     }
		else:
			self.profilepaths = {str(entry).split('.', maxsplit=1)[1]: entry for entry in self.profile_root.iterdir()}

	def _make_file_paths(self):
		self.filepaths = {(profile, file_name): profile_path.joinpath(file_name)
		                  for profile, profile_path in self.profilepaths.items()
		                  for file_name in self.files
		                  }

	def make_paths(self):
		self._make_profile_paths()
		self._make_file_paths()

	def __repr__(self):
		return f'BrowserPaths({self.browser}, {self.files}, {self.profile_root}, {self.profiles})'

def browserpaths_test():
	files = ['places.sqlite', 'permissions.sqlite']
	firefox = BrowserPaths(browser='firefox', files=files,
	                       profile_root='~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles')
	pprint(firefox)
	firefox.make_paths()
	pprint(firefox)
	print('-' * 25)
	profiles_list = ['test_profile0', 'test_profile1']
	firefox = BrowserPaths(browser='firefox', files=files, profile_root='~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles',
	                       profiles=profiles_list)
	firefox.make_paths()
	pprint(repr(firefox))
	pprint(firefox)


if __name__ == '__main__':
	browserpaths_test()

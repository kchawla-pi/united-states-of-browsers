# -*- encoding: utf-8 -*-
"""
Module containing classes to setup browser profile and dtaabase file paths.

Classes: BrowserPaths
"""
from pathlib import Path
from pprint import pprint

from united_states_of_browsers.oops.recon_browsers import print_objects

class BrowserPaths(dict):
	"""	Creates objects to create paths to browser profile and database files.
	Accepts browser name, browser profiles directory path, database files list, browser profiles list (default: all).

	"""
	def __init__(self, browser, profile_root, files, profiles=None):
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

	def _make_firefox_profile_paths(self):
		get_profile_name = lambda dir_entry: str(dir_entry).split(sep='.', maxsplit=1)[1]
		if self.profiles:
			self.profilepaths = {get_profile_name(entry): entry for entry in self.profile_root.iterdir()
			                     for profile in self.profiles
			                     if str(profile).lower() in str(entry).lower()
			                     }
		else:
			self.profilepaths = {get_profile_name(entry): entry for entry in self.profile_root.iterdir()}

	def _make_chrome_profile_paths(self):
		if self.profiles:
			self.profilepaths = {entry.name: entry for entry in self.profile_root.iterdir()}
		else:
			self.profilepaths = {entry.name: entry for entry in self.profile_root.iterdir()
			                     if entry.name.startswith('Profile') or entry.name == 'Default'}

	def _make_file_paths(self):
		self.filepaths = {(profile, file_name): profile_path.joinpath(file_name)
		                  for profile, profile_path in self.profilepaths.items()
		                  for file_name in self.files
		                  }

	def make_paths(self):
		make_path_chooser = {'firefox': self._make_firefox_profile_paths, 'chrome': self._make_chrome_profile_paths}
		make_path_chooser[self.browser]()
		self._make_file_paths()

	def __repr__(self):
		return f'BrowserPaths({self.browser}, {self.files}, {self.profile_root}, {self.profiles})'


def browserpaths_test():
	files = ['places.sqlite', 'permissions.sqlite']
	firefox_all = BrowserPaths(browser='firefox', files=files,
	                       profile_root='~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles')
	firefox_all.make_paths()

	profiles_list = ['test_profile0', 'test_profile1']
	firefox_some = BrowserPaths(browser='firefox', files=files, profile_root='~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles',
	                       profiles=profiles_list)
	firefox_some.make_paths()

	chrome = BrowserPaths(browser='chrome', files=['history'], profile_root='C:\\Users\\kshit\\AppData\\Local\\Google\\Chrome\\User Data')

	objects_list = [firefox_all, firefox_some]
	# print_objects(objects_list)
	print_objects([chrome])





if __name__ == '__main__':
	browserpaths_test()

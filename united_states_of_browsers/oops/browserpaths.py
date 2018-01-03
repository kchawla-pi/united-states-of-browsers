# -*- encoding: utf-8 -*-
"""
Module containing classes to setup browser profile and dtaabase file paths.

Classes: BrowserPaths
"""


class BrowserPaths(dict):
	"""	Creates objects to create paths to browser profile and database files.
	Accepts browser name, browser profiles directory path, database files list, browser profiles list (default: all).

	"""
	def __init__(self, browser, profiles, files, path_crumbs):
		super().__init__(browser=browser, profiles=profiles, files=files, path_crumbs=path_crumbs)
		pass

	def _make_profile_paths(self):
		pass

	def _make_file_paths(self):
		pass

	def make_paths(self):
		self._make_profile_paths()
		self._make_file_paths()


def browserpaths_test():
	pass


if __name__ == '__main__':
	browserpaths_test()

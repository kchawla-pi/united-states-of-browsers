# -*- encoding: utf-8 -*-
"""
Object Oriented version of browser_setup.py . Ease of handling for multiple browsers.
"""
import sys


class Browser:
	def __init__(self, profile_pathcrumbs, database_files):
		""" Accepts the browser name and/or a dict of pathrcrumbs for it.
		Figures out the current platform and chooses pathcrumbs accordingly.
		"""
		self.pathcrumbs = profile_pathcrumbs
		self.files = database_files
		self.os = sys.platform



if __name__ == '__main__':
	browser_info = profile_pathcrumbs_firefox = ['~', 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles']
	chrome_path = f'~\\AppData\\Local\\Google\\Chrome\\User Data\\Default'

	firefox = Browser(profile_pathcrumbs_firefox, ['places.sqlite', 'favicons.sqlite'])

import os
import sqlite3

from collections import namedtuple
from pathlib import Path
from united_states_of_browsers.oops.browser import Browser
from united_states_of_browsers.oops.helpers import make_queries
from united_states_of_browsers.oops.table import Table

from united_states_of_browsers.db_merge.imported_annotations import *


class Orchestrator:
	def __init__(self, appdata_subpath, db_name):
		try:
			self.output_dir = Path(appdata_subpath).expanduser()
		except TypeError as excep:
			self.output_dir = Path(*appdata_subpath).expanduser()
		self.db_name = db_name
		self.profile_paths = None
		self.records_yielders = []
		self.output_db = self.output_dir.joinpath(db_name)
		
	def check_browser_presence(self):
		nt_paths = {'firefox': '~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles',
		            'chrome': '~\\AppData\\Local\\Google\\Chrome\\User Data',
		            'opera': '~\\AppData\\Roaming\\Opera Software',
		            'vivaldi': '~\\AppData\\Local\\Vivaldi\\User Data',
		            }
		if os.name == 'nt':
			paths = nt_paths.copy()
		paths = {browser_name: Path(profile_root).expanduser().absolute() for browser_name, profile_root in paths.items()}
		paths = {browser_name: profile_root for browser_name, profile_root in paths.items() if profile_root.exists()}
		self.profile_paths = paths.copy()

	def make_records_yielders(self):
		if self.profile_paths .get('firefox', None):
			firefox = Browser(browser='firefox', profile_root='~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles', profiles=None,
			                  file_tables={'places.sqlite': ['moz_places', 'moz_bookmarks'], 'favicons.sqlite': ['moz_icons']},
			                  copies_subpath=self.output_dir
			                  )

		records_yielder_fx_moz_places = firefox.access_fields({'moz_places': ['id', 'url', 'title', 'last_visit_date']})
		self.records_yielders.append(records_yielder_fx_moz_places)
		# records_yielder_fx_moz_icons = firefox.access_fields({'moz_icons': ['id', 'icon_url', 'width']})
		
		if self.profile_paths.get('chrome', None):
			chrome = Browser(browser='chrome', profile_root='~\\AppData\\Local\\Google\\Chrome\\User Data', profiles=None,
			                 file_tables={'history': ['urls']},
			                 copies_subpath=self.output_dir
			                 )
			records_yielder_cr_urls = chrome.access_fields({'urls': ['id', 'url', 'title', 'last_visit_time']})
			self.records_yielders.append(records_yielder_cr_urls)
		
		if self.profile_paths.get('opera', None):
			opera = Browser(browser='opera', profile_root='~\\AppData\\Roaming\\Opera Software', profiles=['Opera Stable'],
			                file_tables={'History': ['urls']},
			                copies_subpath=self.output_dir
			                )
			records_yielder_op_urls = opera.access_fields({'urls': ['id', 'url', 'title', 'last_visit_time']})
			self.records_yielders(records_yielder_op_urls)
		
		if self.profile_paths.get('vivaldi', None):
			vivaldi = Browser(browser='vivaldi', profile_root='~\\AppData\\Local\\Vivaldi\\User Data', profiles=None,
			                  file_tables={'History': ['urls']},
			                  copies_subpath=self.output_dir
			                  )
			records_yielder_viv = vivaldi.access_fields({'urls': ['id', 'url', 'title', 'last_visit_time']})
			self.records_yielders.append(records_yielder_viv)

	def write_records(self, tablename, primary_key_name , fieldnames):
		queries = make_queries(tablename, primary_key_name, fieldnames)
		with sqlite3.connect(str(self.output_db)) as connection:
			cursor = connection.cursor()
			cursor.execute(queries['create'])
			[cursor.executemany(queries['insert'], browser_record_yielder) for browser_record_yielder in self.records_yielders]



	def orchestrate(self):
		self.check_browser_presence()
		self.make_records_yielders()
		fieldnames = ['id', 'url', 'title', 'last_visit_date', 'browser', 'profile', 'file', 'tablename']
		# using table as column name seems to conflict with SQL, table_ for example was not giving sqlite3 syntax error on create.
		self.write_records(tablename='history', primary_key_name='rec_num', fieldnames=fieldnames)
		self.build_search_table()






def build_search_table(db_path: PathInfo, included_fieldnames: Sequence[Text]):
	""" Builds virtual table for full-text search in sqlite databases.
	Accepts path to the sqlite file and subset of its fieldnames to be included in the virtual table.
	"""
	table = 'search_table'
	with sqlite3.connect(db_path) as sink_conn:
		column_str = ', '.join(included_fieldnames)
		create_table_query = f'''CREATE VIRTUAL TABLE search_table USING fts5({column_str});'''
		try:
			sink_conn.execute(create_table_query)
		except sqlite3.OperationalError as excep:
			table_exists_text = f'table {table}already exists'
			if table_exists_text in str(excep):
				print(f'{table_exists_text}.')
		sql_placeholder = ('?, ' * len(included_fieldnames))[:-2]
		record_yielder = db_ops.yield_source_records(source_db_paths={'all_merged': db_path},
		                                             source_fieldnames=included_fieldnames,
		                                             )
		virtual_insert_query = f'''INSERT INTO search_table ({column_str}) VALUES ({sql_placeholder})'''
		sink_conn.executemany(virtual_insert_query, tuple(record_yielder))


if __name__ == '__main__':
	appdata_subpath = ('~', 'USB', 'AppData')
	write_combi_db = Orchestrator(appdata_subpath=appdata_subpath, db_name='usb_db.sqlite')
	write_combi_db.orchestrate()
	# build_search_table('combined_db_fx_cr.sqlite', ['id', 'url', 'title', 'last_visit_time'])

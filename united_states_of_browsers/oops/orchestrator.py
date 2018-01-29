import os
import sqlite3

from united_states_of_browsers.oops.browser import Browser
from united_states_of_browsers.oops import browser_data
from united_states_of_browsers.oops.helpers import make_queries

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
		self.installed_browsers_data = None
	
	def find_installed_browsers(self):
		self.installed_browsers_data = [browser_datum
		                                for browser_datum in browser_data.all_browsers
		                                if Path(browser_datum.path).expanduser().absolute().exists()
		                                and browser_datum.os == os.name
		                                ]
	
	def make_records_yielders(self):
		for browser_datum in self.installed_browsers_data:
			each_browser = Browser(browser=browser_datum.browser,
			                       profile_root=browser_datum.path,
			                       profiles=browser_datum.profiles,
			                       file_tables=browser_datum.file_tables,
			                       copies_subpath=self.output_dir)
			each_bowser_records_yielder = each_browser.access_fields(browser_datum.table_fields)
			self.records_yielders.append(each_bowser_records_yielder)
	
	def write_records(self, tablename, primary_key_name, fieldnames):
		queries = make_queries(tablename, primary_key_name, fieldnames)
		with sqlite3.connect(str(self.output_db)) as connection:
			cursor = connection.cursor()
			cursor.execute(queries['create'])
			[cursor.executemany(queries['insert'], browser_record_yielder) for browser_record_yielder in
			 self.records_yielders]
	
	def build_search_table(self):
		search_fields = ['rec_id', 'id', 'url', 'title', 'last_visit_date', 'browser', 'profile', 'file',
		                 'tablename']
		# search_fields = ["url", "title", "visit_count", "last_visit_date"]
		search_fields_str = ", ".join(search_fields)
		create_virtual_query = f'CREATE VIRTUAL TABLE IF NOT EXISTS search_table USING fts5({search_fields_str})'
		read_query = 'SELECT * FROM history WHERE title IS NOT NULL'
		insert_virtual_query = f'INSERT INTO search_table {read_query}'
		with sqlite3.connect(str(self.output_db)) as connection:
			cursor = connection.cursor()
			cursor.execute(create_virtual_query)
			cursor.execute(insert_virtual_query)
	
	def orchestrate(self):
		self.find_installed_browsers()
		self.make_records_yielders()
		fieldnames = ['id', 'url', 'title', 'last_visit_date', 'browser', 'profile', 'file', 'tablename']
		# using table as column name seems to conflict with SQL, table_ for example was not giving sqlite3 syntax error on create.
		self.write_records(tablename='history', primary_key_name='rec_num', fieldnames=fieldnames)
		self.build_search_table()


if __name__ == '__main__':
	appdata_subpath = ('~', 'USB', 'AppData')
	write_combi_db = Orchestrator(appdata_subpath=appdata_subpath, db_name='usb_db.sqlite')
	write_combi_db.orchestrate()
# build_search_table('combined_db_fx_cr.sqlite', ['id', 'url', 'title', 'last_visit_time'])

import os
import sqlite3

from united_states_of_browsers.oops import browser_data
from united_states_of_browsers.oops.browser import Browser
from united_states_of_browsers.oops.helpers import make_queries

from united_states_of_browsers.oops.imported_annotations import *


class Orchestrator:
	def __init__(self, app_path, db_name):
		try:
			self.app_path = Path(app_path).expanduser()
		except TypeError as excep:
			self.app_path = Path(*app_path).expanduser()
		self.db_name = db_name
		self.profile_paths = None
		self.browser_yielder = []
		self.output_db = self.app_path.joinpath(db_name)
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
			                       copies_subpath=self.app_path)
			each_browser_records_yielder = each_browser.access_fields(browser_datum.table_fields)
			self.browser_yielder.append(each_browser_records_yielder)
	
	def write_records(self, tablename, primary_key_name, fieldnames):
		queries = make_queries(tablename, primary_key_name, fieldnames)
		with sqlite3.connect(str(self.output_db)) as connection:
			cursor = connection.cursor()
			cursor.execute(queries['create'])
			[cursor.executemany(queries['insert'], browser_record_yielder)
			 for browser_record_yielder in self.browser_yielder
			 ]
	
	def build_search_table(self):
		search_table_fields_str = ", ".join(browser_data.search_table_fields)
		create_virtual_query = f'CREATE VIRTUAL TABLE IF NOT EXISTS search_table USING fts5({search_table_fields_str})'
		read_query = 'SELECT * FROM history WHERE title IS NOT NULL'
		insert_virtual_query = f'INSERT INTO search_table {read_query}'
		with sqlite3.connect(str(self.output_db)) as connection:
			cursor = connection.cursor()
			cursor.execute(create_virtual_query)
			cursor.execute(insert_virtual_query)
			
	def write_db_path_to_file(self):
		db_path_store = Path(__file__).parents[1].joinpath('AppData', 'merged_db_path.txt')
		with open(db_path_store, 'w') as file_obj:
			file_obj.write(f'{self.output_db.as_posix()}')
			
	
	def orchestrate(self):
		self.find_installed_browsers()
		self.make_records_yielders()
		# using table as column name seems to conflict with SQL, table_ for example was not giving sqlite3 syntax error on create.
		self.write_records(tablename='history', primary_key_name='rec_num', fieldnames=browser_data.history_table_fieldnames)
		self.build_search_table()
		self.write_db_path_to_file()


if __name__ == '__main__':
	app_path = ('~', 'USB')
	write_combi_db = Orchestrator(app_path=app_path, db_name='usb_db.sqlite')
	write_combi_db.orchestrate()
# build_search_table('combined_db_fx_cr.sqlite', ['id', 'url', 'title', 'last_visit_time'])

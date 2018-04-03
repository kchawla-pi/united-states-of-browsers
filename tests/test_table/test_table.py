import sqlite3

from collections import namedtuple
from datetime import datetime as dt
from pathlib import Path
from pprint import pprint

from united_states_of_browsers.db_merge.table import Table

TableArgs = namedtuple('TableArgs', 'table path browser filename profile copies_subpath empty')


class TestTable:
	"""
	Accepts root path & test case info for Table class. Prepares the tests for run.
	**Usage:** TestTable(project_root, test_table_data)
	:param: project_root: root path of a project.
	:param: test_table_data: info for Table test case instatitation.
	**Available tests:**
		test_table_init() is executed automatically.
		
		Tests for Cases with No Exceptions Raised:
			test_table_connect()
			test_table_yield_readable_timestamps()
			test_table_get_records()
			test_table_check_if_db_empty()
	"""
	
	def __init__(self, project_root, test_table_data):
		self.test_data = test_table_data
		self.table_empty = test_table_data.empty
		self.table_obj = self.make_test_table_obj()
		self.test_table_init()
		self.project_root = Path(project_root)
		fullpath = Path(self.project_root, self.test_data.path)
		self.test_data = self.test_data._replace(path=fullpath)
		self.table_obj.path = fullpath
	
	def __str__(self):
		return f"{self.test_data.browser, self.test_data.profile, self.test_data.filename, self.test_data.table,}"
	
	def __repr__(self):
		return f"TestTable({self.project_root}, {self.test_data})"
	
	def make_test_table_obj(self):
		return Table(table=self.test_data.table,
		             path=self.test_data.path,
		             browser=self.test_data.browser,
		             filename=self.test_data.filename,
		             profile=self.test_data.profile,
		             copies_subpath=self.test_data.copies_subpath,
		             )
	
	def test_table_init(self):
		assert self.table_obj.path == self.test_data.path, (repr(self.table_obj.path), repr(self.test_data.path))
		assert self.table_obj.table == self.test_data.table
		assert self.table_obj.browser == self.test_data.browser
		assert self.table_obj.filename == self.test_data.filename
		assert self.table_obj.profile == self.test_data.profile
		assert self.table_obj.copies_subpath == self.test_data.copies_subpath
		return 'test_table_init'
	
	def _get_table_row_yielder_using_table_connect(self):
		connect_exception = self.table_obj._connect()
		conn = self.table_obj._connection
		cur = conn.cursor()
		query = cur.execute(f'SELECT * FROM {self.table_obj.table}')
		row_yielder = query.fetchall()
		return row_yielder, connect_exception
	
	def _get_table_row_yielder_using_sqlite_connect(self):
		conn_arg = f'file:{self.test_data.path}?mode=ro'
		with sqlite3.connect(conn_arg, uri=True) as connection_direct_sql:
			connection_direct_sql.row_factory = sqlite3.Row
			cursor_direct_sql = connection_direct_sql.cursor()
			query_direct_sql = cursor_direct_sql.execute(f'SELECT * FROM {self.test_data.table}')
			query_results_direct_sql = query_direct_sql.fetchall()
			return query_results_direct_sql
	
	def test_table_connect(self):
		row_yielder_sqlite = self._get_table_row_yielder_using_sqlite_connect()
		row_yielder_table, exception_table_connect = self._get_table_row_yielder_using_table_connect()
		assert len(row_yielder_sqlite) == len(row_yielder_table)
		for row_obj_table_method, row_obj_direct_sql in zip(row_yielder_table, row_yielder_sqlite):
			row_direct_sql = dict(row_obj_direct_sql)
			row_table_method = dict(row_obj_table_method)
			assert row_table_method == row_direct_sql, (row_table_method, row_direct_sql)
		return 'connect'
	
	def test_table_yield_readable_timestamps(self):
		row_yielder_raw_timestamps, connect_exception = self._get_table_row_yielder_using_table_connect()
		row_yielder_readable_timestamps = self.table_obj._yield_readable_timestamps(row_yielder_raw_timestamps)
		
		readable_timestamp_rows = list(row_yielder_readable_timestamps)
		orig_raw_timestamp_rows = [dict(raw_timestamp_row_obj) for raw_timestamp_row_obj in row_yielder_raw_timestamps]
		updated_raw_timestamp_rows = []
		for raw_timestamp_row_ in orig_raw_timestamp_rows:
			raw_timestamp = raw_timestamp_row_.get('last_visit_date', raw_timestamp_row_.get('last_visit_time', None))
			if raw_timestamp:
				human_readable_timestamp = str(dt.fromtimestamp(raw_timestamp / 10 ** 6)).split('.')[0]
				raw_timestamp_row_.update(last_visit_readable=human_readable_timestamp)
				updated_raw_timestamp_rows.append(raw_timestamp_row_)
		assert readable_timestamp_rows == updated_raw_timestamp_rows, self.table_obj.browser
		return 'yield_readable_timestamps'
	
	def test_table_get_records(self):
		self.table_obj.get_records()
		
		row_yielder_raw_timestamps, connect_exception = self._get_table_row_yielder_using_table_connect()
		row_yielder_readable_timestamps = self.table_obj._yield_readable_timestamps(row_yielder_raw_timestamps)
		for records_using_get_records, records_directly_yielded in zip(self.table_obj.records_yielder,
		                                                               row_yielder_readable_timestamps):
			assert records_using_get_records == records_directly_yielded, (
				records_using_get_records, records_directly_yielded)
		return 'get_records'
	
	def test_table_check_if_db_empty(self):
		assert self.table_empty == self.table_obj.check_if_db_empty()
		return 'check_if_db_empty'
	

def test_suite_no_exceptions_raised(table_obj, print_testcase=False):
	test_results = [str(table_obj)]
	test_results.append(table_obj.test_table_connect())
	test_results.append(table_obj.test_table_yield_readable_timestamps())
	test_results.append(table_obj.test_table_get_records())
	test_results.append(table_obj.test_table_check_if_db_empty())
	return test_results



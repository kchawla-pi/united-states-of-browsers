import sqlite3

from collections import namedtuple
from pathlib import Path
from pprint import pprint

from united_states_of_browsers.db_merge.table import Table

TableArgs = namedtuple('TableArgs', 'table path browser filename profile copies_subpath')
project_root = Path(__file__).parents[2]


def test_table_init(table_obj, table_arg):
	assert table_obj.path == table_arg.path, (repr(table_obj.path), repr(table_arg.path))
	assert table_obj.table == table_arg.table
	assert table_obj.browser == table_arg.browser
	assert table_obj.filename == table_arg.filename
	assert table_obj.profile == table_arg.profile
	assert table_obj.copies_subpath == table_arg.copies_subpath


def get_table_row_yielder_using_table_connect(table_obj):
	connect_exception = table_obj._connect()
	conn = table_obj._connection
	cur = conn.cursor()
	query = cur.execute(f'SELECT * FROM {table_obj.table}')
	row_yielder = query.fetchall()
	return row_yielder, connect_exception


def get_table_row_yielder_using_sqlite_connect(table_arg):
	with sqlite3.connect(str(table_arg.path)) as connection_direct_sql:
		connection_direct_sql.row_factory = sqlite3.Row
		cursor_direct_sql = connection_direct_sql.cursor()
		query_direct_sql = cursor_direct_sql.execute(f'SELECT * FROM {table_arg.table}')
		query_results_direct_sql = query_direct_sql.fetchall()
		return query_results_direct_sql


def test_table_connect(table_obj, table_arg):
	row_yielder_sqlite = get_table_row_yielder_using_sqlite_connect(table_arg)
	row_yielder_table, exception_table_connect = get_table_row_yielder_using_table_connect(table_obj)
	assert len(row_yielder_sqlite) == len(row_yielder_table)
	for row_obj_table_method, row_obj_direct_sql in zip(row_yielder_table, row_yielder_sqlite):
		row_direct_sql = dict(row_obj_direct_sql)
		row_table_method = dict(row_obj_table_method)
		assert row_table_method == row_direct_sql, (row_table_method, row_direct_sql)


table_arg_no_excep = TableArgs(table='urls',
                      path=Path('tests/data/browser_profiles_for_testing/AppData/Local/Google/Chrome/User Data/Profile 1/History'),
                      browser='chrome',
                      filename='History',
                      profile='Profile 1',
                      copies_subpath=None,
                      )


table_1 = Table(*table_arg_no_excep)
test_table_init(table_obj=table_1, table_arg=table_arg_no_excep)

fullpath = Path(project_root, table_arg_no_excep.path)
table_arg_no_excep = table_arg_no_excep._replace(path=fullpath)
table_2 = Table(*table_arg_no_excep)


test_table_connect(table_2, table_arg_no_excep)

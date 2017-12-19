import sqlite3


class DBFile:
	def __init__(self, dbpath):
		self.dbpath = dbpath
		self.filename = dbpath.name
		self.connection = None
		self.tables_info = None
		self.tables = None
		self.tablenames = None

		self.Table = Table

	def _connect(self):
		with sqlite3.connect(str(self.dbpath)) as conn:
			conn.row_factory = sqlite3.Row
			self.connection = conn

	def _tables_info(self):
		query = 'SELECT * FROM sqlite_master'
		cur = self.connection.cursor()
		result = cur.execute(query)
		self.tables_info = [dict(entry) for entry in result]
		self.tablenames = [table_['name'] for table_ in self.tables_info]

	def _tables_fields(self):
		query = 'SELECT * FROM moz_places'
		cur = self.connection.cursor()
		result = cur.execute(query)
		table = [dict(entry) for entry in result]
		return table

	def read_tables(self):
		self.tables = [self.Table(table_, self.connection) for table_ in self.tablenames]

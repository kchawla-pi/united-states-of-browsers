class Table(object):
	def __init__(self, tablename, connection):
		# super().__init__(tablename=tablename, connection=connection)
		self.tablename = tablename
		self.fieldnames = None
		self.record_yielder = None
		self.connection = connection
		table_data = None

	def get_fieldnames(self):
		# query = 'SELECT * from (?)'
		cur = self.connection.cursor()
		fieldnames = cur.desc
		self.fieldnames = fieldnames

	def yield_record(self):
		query = 'SELECT * from (?)'
		cur = self.connection.cursor()
		result = cur.execute(query, self.tablename)
		self.record_yielder = (dict(record) for record in result)

	def __iter__(self):
		query = 'SELECT * from (?)'
		cur = self.connection.cursor()
		self.record_yielder = cur.execute(query, self.tablename)
		return self

	def __next__(self):
		# next(self.record_yielder, None)
		yield from self.record_yielder

	def __str__(self):
		return f'\{tablename: {self.tablename}, fieldnames: {self.fieldnames}\}'

	def __repr__(self):
		return f'Table({self.tablename})'


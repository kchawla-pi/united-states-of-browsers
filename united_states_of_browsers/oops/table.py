# -*- encoding: utf-8 -*-
import sqlite3


class Table(dict):
	def __init__(self, table, path, browser, file, profile):
		super().__init__(table=table, path=path, browser=browser, file=file, profile=profile)
		self.table = table
		self.path = path
		self.browser = browser
		self.file = file
		self.profile = profile
		self.records_yielder = None
		self._connection = None

	def connect(self):
		""" Connects to the database file using self.path.
		"""
		connection_arg = f'file:{self.path}?mode=ro'
		try:
			with sqlite3.connect(connection_arg) as self._connection:
				self._connection.row_factory = sqlite3.Row
		except sqlite3.OperationalError as excep:
			if 'database is locked' in str(excep).lower():
				print('database is locked')

	def make_records_yielder(self):
		cursor = self._connection.cursor()
		query = f'SELECT * FROM {self.table}'
		self.records_yielder = cursor.execute(query)


def test_table():
	table = Table('1', '2', '3', '4', '5')
	attrs = ('table', 'path', 'browser', 'file', 'profile')
	table2 = Table(table = 'moz_places',
	               path='C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\px2kvmlk.RegularSurfing',
	               browser='firefox',
	               file='places.sqlite',
	               profile='RegularSurfing',
	               )
	print([table[attr_] for attr_ in attrs])
	print(table2)
	print('__str__:', repr(table2))
	print('__repr__:', table2.table)


def test():
	test_table()


if __name__ == '__main__':
	test()

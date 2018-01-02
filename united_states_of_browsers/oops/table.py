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

	def _connect(self):
		""" Connects to the database file using self.path.
		"""
		connection_arg = f'file:{self.path}?mode=ro'
		try:
			with sqlite3.connect(connection_arg, uri=True) as self._connection:
				self._connection.row_factory = sqlite3.Row
		except sqlite3.OperationalError as excep:
			if 'database is locked' in str(excep).lower():
				print('database is locked', '\n', str(self.path))
			else:
				print('\n', str(self.path))
				raise excep

	def _make_records_yielder(self):
		cursor = self._connection.cursor()
		query = f'SELECT * FROM {self.table}'
		self.records_yielder = cursor.execute(query)

	def get_records(self):
		self._connect()
		self._make_records_yielder()


def test_table():
	table = Table('1', '2', '3', '4', '5')


def test_firefox():
	table2 = Table(table='moz_places',
	               path='C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\px2kvmlk.RegularSurfing\\places.sqlite',
	               browser='firefox',
	               file='places.sqlite',
	               profile='RegularSurfing',
	               )
	table2.get_records()
	for record_yielder in table2.records_yielder:
		pass
		# print(dict(record_yielder))

	table3 = Table(table='moz_places',
	               path='C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\e0pj4lec.test_profile0\\places.sqlite',
	               browser='firefox',
	               file='places.sqlite',
	               profile='test_profile0',
	               )
	table3.get_records()
	for record_yielder in table3.records_yielder:
		pass
		# print(dict(record_yielder))

	table4 = Table(table='moz_places',
	               path='C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\udd5sttq.test_profile2\\places.sqlite',
	               browser='firefox',
	               file='places.sqlite',
	               profile='test_profile0',
	               )
	table4.get_records()
	for record_yielder in table4.records_yielder:
		pass
		print(dict(record_yielder))

	table5 = Table(table='moz_places',
	               path='C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\kceyj748.test_profile1\\places.sqlite',
	               browser='firefox',
	               file='places.sqlite',
	               profile='test_profile0',
	               )
	table5.get_records()
	for record_yielder in table5.records_yielder:
		pass
		print(dict(record_yielder))

def test_chrome():
	table2 = Table(table='urls',
	               path='C:\\Users\\kshit\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\history',
	               browser='chrome',
	               file='history',
	               profile='Default',
	               )
	table2.get_records()
	for record_yielder in table2.records_yielder:
		print(dict(record_yielder))


def print_table_attr(obj):
	attrs = ('table', 'path', 'browser', 'file', 'profile')
	print([obj[attr_] for attr_ in attrs])
	print(obj)
	print('__str__:', repr(obj))
	print('__repr__:', obj.table)


def test():
	test_table()
	test_firefox()
	# test_chrome()


if __name__ == '__main__':
	test()

# -*- encoding: utf-8 -*-

import sqlite3

from pathlib import Path

from united_states_of_browsers.oops.exceptions_handling import invalid_path_in_tree


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
		""" Creates TableObject.connection to the database file specified in TableObject.path.
		Returns Exception on error.
		"""
		connection_arg = f'file:{self.path}?mode=ro'
		try:
			with sqlite3.connect(connection_arg, uri=True) as self._connection:
				self._connection.row_factory = sqlite3.Row
		except sqlite3.OperationalError as excep:
			if 'database is locked' in str(excep).lower():
				print('database is locked', '\n', str(self.path))
				raise excep
			elif 'unable to open database file' in str(excep).lower():
				invalid_path = invalid_path_in_tree(self.path)
				if invalid_path:
					return OSError(f'Path does not exist: {invalid_path}')
				elif not self.path.is_file():
					return OSError(f'{self.path.name} is not a file')
				else:
					raise excep

	def _make_records_yielder(self):
		""" Yields a generator of all fields in TableObj.table
		"""
		cursor = self._connection.cursor()
		query = f'SELECT * FROM {self.table}'
		self.records_yielder = cursor.execute(query)

	def get_records(self):
		""" Yields a generator to all fields in TableObj.table.
		"""
		exception_raised = self._connect()
		if exception_raised:
			print(f'{exception_raised}.\n Moving on ...')
		else:
			self._make_records_yielder()


def test_table():
	table = Table('1', '2', '3', '4', '5')


def test_firefox():
	table2 = Table(table='moz_places',
	               path=Path('C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\px2kvmlk.RegularSurfing_glitch\\places.sqlite'),
	               browser='firefox',
	               file='places.sqlite',
	               profile='RegularSurfing',
	               )
	table2.get_records()
	# for record_yielder in table2.records_yielder:
	# 	pass
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
	# table4.get_records()
	# for record_yielder in table4.records_yielder:
	# 	pass
	# 	print(dict(record_yielder))

	table5 = Table(table='moz_places',
	               path='C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\kceyj748.test_profile1\\places.sqlite',
	               browser='firefox',
	               file='places.sqlite',
	               profile='test_profile0',
	               )
	table5.get_records()
	for record_yielder in table5.records_yielder:
		pass
		# print(dict(record_yielder)['url'])

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

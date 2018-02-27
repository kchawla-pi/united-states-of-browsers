import sqlite3

from pprint import pprint


from united_states_of_browsers.db_merge import exceptions_handling as exceph
"""
try:
	with sqlite3.connect(connection_arg, uri=True) as self._connection:
		self._connection.row_factory = sqlite3.Row
except sqlite3.OperationalError as excep:
	if 'database is locked' in str(excep).lower():
		print('database is locked', '\n', str(self.path))
		raise excep
	elif 'unable to open database file' in str(excep).lower():
		invalid_path = exceph.invalid_path_in_tree(self.path)
		if invalid_path:
			return OSError(f'Path does not exist: {invalid_path}')
		elif not self.path.is_file():
			return OSError(errno.ENOENT,
			               f'"{self.path.name}" is not a file, or the file does not exist. The profile "{self.profile}" might not contain any data.',
			               str(
				               self.path))  # excep, f'{self.path.name} is not a file, or the file does not exist. The profile might not contain any data. ({self.path})')
		else:
			raise
	else:
		raise

"""


class SQLiteError(sqlite3.OperationalError):
	def __init__(self, path=None):
		self.msg = str(self).lower()
		self.path = path
		self.invalid_path = exceph.invalid_path_in_tree(path)
		super().__init__(self.args, path)
		self.parse_exception()
	
	def parse_exception(self):
		if 'database is locked' in self.msg:
			raise DatabaseLockedError(self)
		elif 'unable to open database file' in self.msg and self.invalid_path:
			raise InvalidPathError(self)
		elif 'unable to open database file' in self.msg and not self.path.is_file():
			raise InvalidDatabaseFileError(self)
		else:
			print('SQLiteError_else')
			raise self
	# try: except sqlite error, send excep to func which returns specific exep, the riase that


class DatabaseLockedError(SQLiteError):
	def __init__(self, filepath=None):
		self.filepath = filepath
		super().__init__(self, filepath)
	
	def __str__(self):
		return (f'Unable to open database file. '
		        f'Database is locked and in use by some other process.\n'
		        f'{self.filepath}'
		        )
	
	
class InvalidPathError(SQLiteError):
	def __init__(self, filepath=None):
		self.filepath = filepath
		super().__init__(self, filepath)
		
	def __str__(self):
		return (f'Unable to open database file. '
		        f'The path to the database file does not exist.\n'
		        f'{self.filepath}'
		        )
	
	
class InvalidDatabaseFileError(SQLiteError):
	def __init__(self, filepath=None):
		self.filepath = filepath
		super().__init__(self, filepath)
		
	def __str__(self):
		return (f'Unable to open database file. '
		        f'The file is not an SQLite database file, or it does not exist.\n'
		        f'{self.filepath}'
		        )


def sqlite_operational_error(dbpath):
	try:
		conn = sqlite3.connect(dbpath)
	except sqlite3.OperationalError as excep:
		print('sqlite3.OperationalError')
		raise excep
	else:
		return conn
	finally:
		print('sqlite_operational_error')


def sqlite_error(dbpath):
	try:
		conn = sqlite3.connect(dbpath)
	except SQLiteError(path=dbpath) as excep:
		print(excep)
		raise excep
	else:
		return conn
	finally:
		print('sqlite_error')
	

def sqlite_specific_error(dbpath):
	try:
		conn = sqlite3.connect(dbpath)
	except DatabaseLockedError as excep:
		raise excep
	except InvalidDatabaseFileError as excep:
		raise excep
	except InvalidPathError as excep:
		raise excep
	else:
		return conn
	finally:
		print('sqlite_specific_error')

if __name__ == '__main__':
	dbpath = '~/OneDrive/Desktop/somthing/wicked/db'
	# conn = sqlite_operational_error(dbpath)
	conn = sqlite_error(dbpath)
	conn = sqlite_specific_error(dbpath)

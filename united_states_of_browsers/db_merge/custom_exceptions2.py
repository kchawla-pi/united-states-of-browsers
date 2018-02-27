import sqlite3
import sys

from united_states_of_browsers.db_merge import exceptions_handling as exceph


class DatabaseLockedError(sqlite3.OperationalError):
	def __init__(self):
		self.msg = str(self).lower()
		if 'database is locked' in self.msg:
			super().__init__(self)
			raise self

	def __str__(self):
		return (f'Unable to open database file. '
		        f'Database is locked and in use by some other process.\n'
		        f'{self.filepath}'
		        )


class InvalidPathError(sqlite3.OperationalError):
	def __init__(self):
		self.msg = str(self).lower()
		self.invalid_path = exceph.invalid_path
		if 'unable to open database file' in self.msg and self.invalid_path:
			super().__init__(self)
			raise self
	
	def __str__(self):
		return (f'Unable to open database file. '
		        f'The path to the database file does not exist.\n'
		        f'{self.filepath}'
		        )


class InvalidDatabaseFileError(sqlite3.OperationalError):
	def __init__(self):
		self.msg = str(self).lower()
		if 'unable to open database file' in self.msg and not self.path.is_file():
			super().__init__(self)
			raise self
		
	def __str__(self):
		return (f'Unable to open database file. '
		        f'The file is not an SQLite database file, or it does not exist.\n'
		        f'{self.filepath}'
		        )
	

def sqlite_specific_error(dbpath):
	try:
		conn = sqlite3.connect(dbpath)
	except Exception as excep:
		print(sys.exc_info)
		excep
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


def sqlite_specific_error_function(dbpath):
	try:
		conn = sqlite3.connect(dbpath)
	except sqlite3.OperationalError as excep:
		raise exceph.sqlite_operational_errors(excep, dbpath)


if __name__ == '__main__':
	dbpath = '~/OneDrive/Desktop/somthing/wicked/db'
	sqlite_specific_error_function(dbpath)
	# sqlite_specific_error(dbpath)

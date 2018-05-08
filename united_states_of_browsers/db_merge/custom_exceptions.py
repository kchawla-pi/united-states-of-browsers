import sqlite3
from pathlib import Path


class DatabaseLockedError(sqlite3.OperationalError):
	def __init__(self, exception_obj, path, browsername='browser'):
		self.path = path
		self.browsername = browsername
		self.exception_obj = exception_obj
	
	def __str__(self):
		return (
			f'\n\nUnable to open database file: `{self.path.name}`\n  for `{self.browsername}` \nat `{self.path.parent}`\n'
			f'Database is locked and in use by some other process.\n'
			)


class InvalidFileError(sqlite3.DatabaseError, FileNotFoundError):
	def __init__(self, exception_obj, error_symbol, path, browsername, profilename):
		self.error_symbol = error_symbol
		self.path = Path(path)
		self.profilename = profilename
		self.browsername = browsername
		self.exception_obj = exception_obj
	
	def __str__(self):
		return (
			f'\n\n`{self.path.name}` is not a sqlite3 database file, or the file does not exist.\n'
			f'Attempted to open: {self.path} .\n'
			f'The {self.browsername} profile `{self.profilename}` may be empty.\n'
			)


class InvalidPathError(FileNotFoundError):
	def __init__(self, exception_obj, error_symbol, path, browsername, profilename, invalid_path):
		self.error_symbol = error_symbol
		self.path = Path(path)
		self.profilename = profilename
		self.browsername = browsername
		self.exception_obj = exception_obj
		self.invalid_path = invalid_path
	
	def __str__(self):
		return f'\n\nPath does not exist: {self.invalid_path}\n'


class InvalidTableError(sqlite3.OperationalError):
	def __init__(self, exception_obj, path, tablename, browsername, profilename):
		self.path = Path(path)
		self.tablename = tablename
		self.browsername = browsername
		self.profilename = profilename
		self.exception_obj = exception_obj
	
	def __str__(self):
		return (f'\n\nTable `{self.tablename}` does not exist in `{self.path.name}.`\n'
		        f'The `{self.browsername}` profile `{self.profilename}` may be empty.\n'
		        )

# excep = DatabaseLockedError()
# print(excep)

import sqlite3
from pathlib import Path

class DatabaseLockedError(sqlite3.OperationalError):
	def __init__(self, exception_obj,  path, browsername='browser'):
		self.path = path
		self.browsername = browsername
		self.exception_obj = exception_obj
	def __str__(self):
		return (f'Unable to open database file: `{self.path.name}`\n  for `{self.browsername}` \nat `{self.path.parent}`\n'
		        f'Database is locked and in use by some other process.\n'
		        )


class InvalidTableError(sqlite3.OperationalError):
	def __init__(self, exception_obj, path, tablename, browsername, profilename):
		self.path = Path(path)
		self.tablename = tablename
		self.browsername = browsername
		self.profilename = profilename
		self.exception_obj = exception_obj
		
	def __str__(self):
		return (f'Table `{self.tablename}` does not exist in `{self.path.name}.`\n'
		        f'The `{self.browsername}` profile `{self.profilename}` may be empty.'
		        )

# excep = DatabaseLockedError()
# print(excep)

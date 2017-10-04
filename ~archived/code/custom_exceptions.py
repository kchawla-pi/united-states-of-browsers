import sqlite3


class MissingDatabaseTableError(sqlite3.OperationalError):
	def __init__(self, *args, **kwargs):
		Exception.__init__(self, *args, **kwargs)
		if args[0]:
			self.arg1 = args[0]

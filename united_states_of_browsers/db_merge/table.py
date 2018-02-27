# -*- encoding: utf-8 -*-

import errno
import shutil
import sqlite3

from datetime import datetime as dt
from pathlib import Path
from pprint import pprint

from united_states_of_browsers.db_merge import exceptions_handling as exceph
from united_states_of_browsers.db_merge.imported_annotations import *

class Table(dict):
	""" Table object for SQLite database files.
	
	Usage:
		table_obj = Table(table, path, browser, filename, profile)
		
		table_obj.get_records()
		
		for record in **table_obj.records_yielder**:  # a records yielding generator
			print(record)
	
	:param: table: Name of the target table in the sqlite database file.
	:param: path: Path to the sqlite database file, **including filename**.
	:param: browser: Browser name, to which the database file belongs.
	:param: filename: name of the sqlite database file.
	:param: profile: Name of the browser profile who's data is being accessed.
	:param: copies_subpath: Optional. If a valid directory path is given, creates a copy of the SQLite database to read from.
	
	
	"""
	def __init__(self,
	             table: Text,
	             path: PathInfo,
	             browser: Text,
	             filename: Text,
	             profile: Text,
	             copies_subpath: Optional[PathInfo]=None
	             ) -> None:
		super().__init__(table=table, path=path, browser=browser, file=filename, profile=profile)
		self.table = table
		self.path = Path(path)
		self.orig_path = Path(path)
		self.browser = browser
		self.filename = filename
		self.profile = profile
		self.copies_subpath = copies_subpath
		self.records_yielder = None
		self._connection = None
		
	def _create_db_copy(self):
		dst = Path(self.copies_subpath, 'AppData', 'Profile Copies', self.browser, self.profile).expanduser()
		dst.mkdir(parents=True, exist_ok=True)
		try:
			self.path = Path(shutil.copy2(self.path, dst))
		except FileNotFoundError as excep:
			return FileNotFoundError(errno.ENOENT,
			                         f'File {self.path.name} does not exist for {self.browser} profile "{self.profile}". The profile may be empty.',
			                         str(self.path))
		except shutil.SameFileError as excep:
			self.path = dst.joinpath(self.path.name)

	def _connect(self):
		""" Creates TableObject.connection to the database file specified in TableObject.path.
		Returns Exception on error.
		"""

		connection_arg = f'file:{self.path}?mode=ro'
		files_pre_connection_attempt = set(entry for entry in self.path.parents[1].iterdir() if entry.is_file())
		try:
			with sqlite3.connect(connection_arg, uri=True) as self._connection:
				self._connection.row_factory = sqlite3.Row
		except sqlite3.OperationalError as excep:
			return exceph.sqlite3_operational_errors(excep, self.path, self.profile)  # returns a loggable error or raises a fatal one.
		finally:
			# Cleans up any database files created during failed connection attempt.
			exceph.remove_new_empty_files(dirpath=self.path.parents[1], existing_files=files_pre_connection_attempt)

	def _make_records_yielder(self) -> Generator:
		""" Yields a generator of all fields in TableObj.table
		"""
		cursor = self._connection.cursor()
		query = f'SELECT * FROM {self.table}'
		records_yielder = cursor.execute(query)
		# self.records_yielder = (dict(record) for record in records_yielder)
		for record in records_yielder:
			record_dict = dict(record)
			timestamp_ = record_dict.get('last_visit_date', record_dict.get('last_visit_time', None))
			try:
				human_readable = dt.fromtimestamp(timestamp_ / 10 ** 6 )
			except TypeError as excep:
				pass  # reocrds without valid timestamps are removed down the process
			except OSError as excep:
				pass  # reocrds without valid timestamps are removed down the process
			record_dict.update({'last_visit_readable': str(human_readable).split('.')[0]})
			yield record_dict
	

	def get_records(self):
		""" Yields a generator to all fields in TableObj.table.
		"""
		if self.copies_subpath:
			file_copy_exception_raised = self._create_db_copy()
			if file_copy_exception_raised:
				return file_copy_exception_raised
		db_connect_exception_raised = self._connect()
		if db_connect_exception_raised:
			return db_connect_exception_raised
		else:
			try:
				self.records_yielder = self._make_records_yielder()
			except sqlite3.OperationalError as excep:
				if 'no such table' in str(excep):
					return ValueError(
						f'Table "{self.table}" does not exist in database file "{self.filename}" in '
						f'{self.browser} profile "{self.profile}". The profile may be empty.'
							)
				return None

	def check_if_db_empty(self):
		cursor = self._connection.cursor()
		query = f'SELECT name FROM sqlite_master WHERE type = "table"'
		query_results = cursor.execute(query).fetchall()
		all_tables = [tuple(result_)[0] for result_ in query_results]
		return False if all_tables else True


if __name__ == '__main__':
	table4 = Table(table='moz_places',
	               path='C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\a2o7b88n.Employment\\places.sqlite',
	               browser='firefox',
	               filename='places.sqlite',
	               profile='Employment',
	               )
	table4.get_records()
	pprint(list(table4.records_yielder))
	quit()
# [record for browser_record_yielder in self.browser_yielder for record in browser_record_yielder]
	# test()

# -*- encoding: utf-8 -*-

import errno
import pytest
import shutil
import sqlite3

from collections import namedtuple
from datetime import datetime as dt
from pathlib import Path


# ---------- Imported Annotations ----------------------

from os import PathLike
from typing import (Any,
                    AnyStr,
                    ByteString,
                    Dict,
                    Generator,
                    Iterable,
                    List,
                    Mapping,
                    NamedTuple,
                    Optional,
                    Sequence,
                    SupportsInt,
                    Text, Tuple, Type, TypeVar,
                    Union,
                    NewType,
                    )

PathInfo = NewType('PathInfo', Union[Path, PathLike, Text, ByteString])


class BrowserData(NamedTuple):
	os: Text
	browser: Text
	path: PathInfo
	profiles: Optional[Iterable[Text]]
	file_tables: Mapping[Text, Iterable[Text]]
	table_fields: Mapping[Text, Iterable[Text]]

# ------------------- Exception hanling functions -------------------------


def invalid_path_in_tree(path_to_test: PathInfo) -> AnyStr:
	""" Accepts a path and returns the first invalid parent.
	"""
	path_to_test = Path(path_to_test)
	first_invalid_path_in_tree = [path_parent for path_parent in path_to_test.parents if
	                              not path_parent.exists() or not path_parent.is_dir()]
	return first_invalid_path_in_tree[-1] if first_invalid_path_in_tree else None


def remove_new_empty_files(dirpath: PathInfo, existing_files: Iterable[Text]) -> None:
	""" Deletes any newly created files of size zero. Useful in removing files created during an aborted process.
	Accepts the directory where the files are present and the list of files in it before the process was initiated.
	"""
	dirpath = Path(dirpath)
	files_post_connection_attempt = set(entry for entry in dirpath.iterdir() if entry.is_file())
	extra_files = files_post_connection_attempt.difference(existing_files)
	[file_.unlink() for file_ in extra_files if file_.stat().st_size == 0]


def exceptions_log_deduplicator(exceptions_log: Iterable):
	unique_exception_strings = {str(excep_): excep_ for excep_ in exceptions_log}
	return list(unique_exception_strings.values())


def sqlite3_operational_errors_handler(exception_obj: Exception, calling_obj: object) -> Optional[Exception]:
	""" Returns or raises useful exception subtype from sqlite3.OperationalError .
	Accepts sqlite3.OperationalError exception object and path of the sqlite3 database file.
	"""
	tablename = calling_obj['table']
	browsername = calling_obj['browser']
	profilename = calling_obj['profile']
	path = calling_obj['path']
	
	msg = str(exception_obj).lower()
	invalid_path = invalid_path_in_tree(path)
	
	if 'unable to open database' in msg and invalid_path:
		raise OSError(f'Path does not exist: {invalid_path}')
	if 'unable to open database' in msg and not invalid_path:
		raise OSError(errno.ENOENT,
		              f'`{path.name}` is not a sqlite3 database file, or the file does not exist.\n'
		              f'Attempted to open: {path} .\n'
		              f'The profile `{profilename}` may be empty.',
		              ) from sqlite3.OperationalError
	if 'no such table' in msg:
		return InvalidTableError(exception_obj, path, tablename=tablename, browsername=browsername,
		                         profilename=profilename)
	if 'database is locked' in msg:
		raise DatabaseLockedError(exception_obj, path, browsername=browsername) from sqlite3.OperationalError
	raise exception_obj


# ------------------ Custom Exception --------------------------------------

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

class DatabaseLockedError(sqlite3.OperationalError):
	def __init__(self, exception_obj,  path, browsername='browser'):
		self.path = path
		self.browsername = browsername
		self.exception_obj = exception_obj
	def __str__(self):
		return (f'Unable to open database file: `{self.path.name}`\n  for `{self.browsername}` \nat `{self.path.parent}`\n'
		        f'Database is locked and in use by some other process.\n'
		        )

# ----------------- Table class, which does the actual work ----------------------------------

class Table(dict):
	""" Table object for SQLite database files.

	Usage:
		table_1 = Table(table, path, browser, filename, profile)

		table_1.get_records()

		for record in **table_1.records_yielder**:  # a records yielding generator
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
	             copies_subpath: Optional[PathInfo] = None
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
			return sqlite3_operational_errors_handler(exception_obj=excep,
			                                                 calling_obj=self)  # returns a loggable error or raises a fatal one.
		finally:
			# Cleans up any database files created during failed connection attempt.
			remove_new_empty_files(dirpath=self.path.parents[1], existing_files=files_pre_connection_attempt)
	
	def _yield_readable_timestamps(self, records_yielder) -> Generator:
		""" Yields a generator of records for TableObj.table with a with a readable timestamp.
		Accepts a generator of table records with a valid timestamp.
		"""
		for record in records_yielder:
			record_dict = dict(record)
			timestamp_ = record_dict.get('last_visit_date', record_dict.get('last_visit_time', None))
			try:
				human_readable = dt.fromtimestamp(timestamp_ / 10 ** 6)
			except TypeError as excep:
				continue
				pass  # records without valid timestamps are removed
			except OSError as excep:
				continue
				pass  # records without valid timestamps are removed
			
			record_dict.update({'last_visit_readable': str(human_readable).split('.')[0]})
			yield record_dict
	
	def get_records(self, raise_exceptions=True):
		""" Yields a generator to all fields in TableObj.table.
		"""
		if self.copies_subpath:
			file_copy_exception_raised = self._create_db_copy()
			if file_copy_exception_raised:
				return self.records_yielder, file_copy_exception_raised
		db_connect_exception_raised = self._connect()
		if db_connect_exception_raised:
			return db_connect_exception_raised
		else:
			cursor = self._connection.cursor()
			query = f'SELECT * FROM {self.table}'
			try:
				records_yielder = cursor.execute(query)
			except sqlite3.OperationalError as excep:
				exception_raised = sqlite3_operational_errors_handler(exception_obj=excep, calling_obj=self)
			else:
				self.records_yielder = self._yield_readable_timestamps(records_yielder)
				exception_raised = None
			if raise_exceptions and exception_raised:
				raise exception_raised
			else:
				return self.records_yielder, exception_raised
	
	def check_if_db_empty(self):
		cursor = self._connection.cursor()
		query = f'SELECT name FROM sqlite_master WHERE type = "table"'
		query_results = cursor.execute(query).fetchall()
		all_tables = [tuple(result_)[0] for result_ in query_results]
		return False if all_tables else True


# --------------------- Testing Table --------------------------

TableArgs = namedtuple('TableArgs', 'table path browser filename profile copies_subpath')
project_root = Path(__file__).parents[2]


test_cases_exception_no_such_table = [
	TableArgs(table='moz_places',
	          path=Path(project_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Roaming/Mozilla/'
	                    'Firefox/Profiles/udd5sttq.test_profile2/non_db_dummy_file_for_testing.txt'),
	          browser='firefox',
	          filename='non_db_dummy_file_for_testing.txt',
	          profile='test_profile2',
	          copies_subpath=None,
	          ),
	TableArgs(table='nonexistent_table',
	          path=Path(project_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Local/Google/Chrome/User Data/Profile 1/History'),
	          browser='chrome',
	          filename='History',
	          profile='Profile 1',
	          copies_subpath=None,
	          ),
	TableArgs(table='urls',
	          path=Path(project_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Local/Vivaldi/User Data/Default/History'),
	          browser='vivaldi',
	          filename='History',
	          profile='Default',
	          copies_subpath=None,
	          ),
	]


@pytest.mark.parametrize('test_case', [test_case for test_case in test_cases_exception_no_such_table])
def test_connect(test_case):
	table_obj = Table(*test_case)
	with pytest.raises(sqlite3.DatabaseError) as excep:
		table_obj.get_records()


def non_pytest_test_connect():
	for test_case in test_cases_exception_no_such_table:
		table_obj = Table(*test_case)
		try:
			table_obj.get_records()
		except sqlite3.DatabaseError as excep:
			print(excep, '--', test_case.browser, test_case.profile, test_case.filename, test_case.table)
		else:
			print('No error.', '--', test_case.browser, test_case.profile, test_case.filename, test_case.table)
		finally:
			print()
			# assert str(excep) == 'file is not a database'

# --------------- Functions I wrote tryin to troubleshoot this problem -----------------------------------------

def raising_errors():
	for test_case in test_cases_exception_no_such_table:
		table_obj = Table(*test_case)
		table_obj.get_records()

def test_raising_errors():
	with pytest.raises(sqlite3.DatabaseError) as excep:
		raising_errors()


if __name__ == '__main__':
	# non_pytest_test_connect()
	raising_errors()
	test_raising_errors()

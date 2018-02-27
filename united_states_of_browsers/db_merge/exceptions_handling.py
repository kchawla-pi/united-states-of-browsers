import errno
import sqlite3

from pathlib import Path
from pprint import pprint
from united_states_of_browsers.db_merge.imported_annotations import *


def invalid_path_in_tree(path_to_test: PathInfo) -> AnyStr:
	""" Accepts a path and returns the first invalid parent.
	"""
	path_to_test = Path(path_to_test)
	first_invalid_path_in_tree = [path_parent for path_parent in path_to_test.parents if not path_parent.exists() or not path_parent.is_dir()]
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


def sqlite3_operational_errors(exception_obj: Exception, path: PathInfo) -> Optional[Exception]:
	""" Returns or raises useful exception subtype from sqlite3.OperationalError .
	Accepts sqlite3.OperationalError exception object and path of the sqlite3 database file.
	"""
	class DatabaseLockedError(sqlite3.OperationalError):
		def __str__(self):
			return (f'Unable to open database file. '
			        f'Database is locked and in use by some other process.\n'
			        f'{path}'
			        )
	msg = str(exception_obj).lower()
	invalid_path = invalid_path_in_tree(path)
	
	if 'unable to open database' in msg and invalid_path:
		return OSError(f'Path does not exist: {invalid_path}')
	if 'unable to open database' in msg and not invalid_path:
		return OSError(errno.ENOENT, f'"{self.path.name}" is not a sqlite3 database file, or the file does not exist.{path}')
	if 'database is locked' in msg:
		raise DatabaseLockedError(path)	from sqlite3.OperationalError
	raise exception_obj
	
	
def test_path_tester():
	paths_to_test = ('C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\px2kvmlk.RegularSurfing\\places.sqlite',)
	curr_path_to_test = paths_to_test[0]
	print(repr(invalid_path_in_tree(curr_path_to_test)))


if __name__ == '__main__':
	test_path_tester()

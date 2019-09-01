# -*- encoding: utf-8 -*-

import errno
import shutil
import sqlite3
from datetime import datetime as dt

from united_states_of_browsers.db_merge import exceptions_handling as exceph
from united_states_of_browsers.db_merge.imported_annotations import *


class Table(dict):
    """ Table object for SQLite database files.
    
    Usage:
        table_1 = Table(table, path, browser, filename, profile)
        
        table_1.make_records_yielder()
        
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
        except FileNotFoundError:
            return FileNotFoundError(errno.ENOENT,
                                     f'File {self.path.name} does not exist for {self.browser} profile "{self.profile}". The profile may be empty.',
                                     str(self.path))
        except shutil.SameFileError as excep:
            self.path = dst.joinpath(self.path.name)
    
    def _connect(self):
        """ Creates TableObject.connection to the database file specified in TableObject.path.
        Returns Exception on error.
        """
        
        try:
            files_pre_connection_attempt = set(entry for entry in self.path.parents[1].iterdir() if entry.is_file())
        except FileNotFoundError as excep:
            exception_raised = exceph.return_more_specific_exception(exception_obj=excep,
                                                                     calling_obj=self)
            return exception_raised  # returns a loggable error or raises a fatal one.
        
        db_file_path_uri_mode = f'file:{self.path}?mode=ro'
        try:
            with sqlite3.connect(db_file_path_uri_mode, uri=True) as self._connection:
                self._connection.row_factory = sqlite3.Row
        except sqlite3.OperationalError as excep:
            exception_raised = exceph.return_more_specific_exception(exception_obj=excep,
                                                                     calling_obj=self)  # returns a loggable error or raises a fatal one.
            return exception_raised
        finally:
            # Cleans up any database files created during failed connection attempt.
            exceph.remove_new_empty_files(dirpath=self.path.parents[1], existing_files=files_pre_connection_attempt)
    
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
            except OSError:
                continue  # records without valid timestamps are removed
            
            record_dict.update({'last_visit_readable': str(human_readable).split('.')[0]})
            yield record_dict
    
    def make_records_yielder(self, raise_exceptions=True):
        """ Yields a generator to all fields in TableObj.table.
        """
        if self.copies_subpath:
            file_copy_exception_raised = self._create_db_copy()
            if file_copy_exception_raised:
                return self.records_yielder, file_copy_exception_raised
        db_connect_exception_raised = self._connect()
        if db_connect_exception_raised:
            raise db_connect_exception_raised
        else:
            cursor = self._connection.cursor()
            query = f'SELECT * FROM {self.table}'
            try:
                records_yielder = cursor.execute(query)
            except (sqlite3.OperationalError, sqlite3.DatabaseError) as excep:
                exception_raised = exceph.return_more_specific_exception(exception_obj=excep, calling_obj=self)
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


if __name__ == '__main__':  # pragma: no cover
    table4 = Table(table='moz_places',
                   path='C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\a2o7b88n.Employment\\places.sqlite',
                   browser='firefox',
                   filename='places.sqlite',
                   profile='Employment',
                   )
    table4.make_records_yielder()
    table4_records = list(table4.records_yielder)
    print(len([record for record in table4_records if record['title'] and record['last_visit_date']]))
    print(len([record for record in table4_records if not (record['title'] and record['last_visit_date'])]))
    print(len([record for record in table4_records if not (record['last_visit_date'])]))
    print(len([record for record in table4_records if not (record['title'])]))
    
    table2 = Table(table='moz_places',
                   path=Path(
                           'C:\\Users\\kshit\\OneDrive\\workspace\\UnitedStatesOfBrowsers\\'
                           'tests/data/browser_profiles_for_testing/AppData/Roaming/Mozilla/'
                           'Firefox/Profiles/udd5sttq.test_profile2/non_db_dummy_file_for_testing.txt'),
                   browser='firefox',
                   filename='non_db_dummy_file_for_testing.txt',
                   profile='test_profile2',
                   copies_subpath=None,
                   )
    # table2.make_records_yielder()
    
    table3 = Table(table='moz_places',
                   path=Path(
                           'C:\\Users\\kshit\\OneDrive\\workspace\\UnitedStatesOfBrowsers\\'
                           'tests/data/browser_profiles_for_testing/AppData/Roaming/Mozilla/'
                           'Firefox/Profiles/udd5sttq.test_profile2/non_db_dummy_file_for_testing.txt'),
                   browser='firefox',
                   filename='non_db_dummy_file_for_testing.txt',
                   profile='test_profile2',
                   copies_subpath=None,
                   )
# table3.make_records_yielder()

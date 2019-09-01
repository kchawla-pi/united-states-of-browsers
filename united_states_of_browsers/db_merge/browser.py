# -*- encoding: utf-8 -*-
"""
The Browser class
"""
from collections import namedtuple

from united_states_of_browsers.db_merge.browserpaths import BrowserPaths
from united_states_of_browsers.db_merge.table import Table
from united_states_of_browsers.db_merge import exceptions_handling as exceph
from united_states_of_browsers.db_merge.imported_annotations import *


TableMetadata = namedtuple('TableMetadata', 'browser profile file table')

class Browser(dict):
    """ Creates a generator of browser database records.
    Accepts parameters-
        :param: browser: browser name
        :param: profile_root: path to directory/folder where the browser stores all of its profiles
        :param: profiles: list of profile, default is all profiles
        :param: file_tables: dict of database file name containing the tables as keys, list of tables to be accessed as values.
        :param: copies_subpath: path where a copy of the database files is created, and read from,instead of the original files.

    **Methods:**
        make_paths()
        
        access_table(file, tables)

    **Usage:**
        browser_obj = Browser(browser, profile_root, profiles, {database_file1: [table1, table2], database_file2: [table3, table4]})

    Add additional file and tables to existing Browser objects using the access_table() method.
            browser_obj.access_table(database_file1, [table1, table2])
            
    Access each table:
        for table in browser_obj.tables:
            for record in table.records_yielder:
                dict(record)
            
    """
    
    def __init__(self, browser: Text, profile_root: PathInfo, profiles: Optional[Iterable[Text]]=None,
                 file_tables: Dict[Text, Iterable[Text]]=None, copies_subpath: Optional[PathInfo]=None):
        self.browser = browser
        self.profile_root = profile_root
        self.profiles = profiles
        self.file_tables = file_tables
        self.files = None
        self.paths = None
        self.tables = []
        self.copies_subpath = copies_subpath
        self.make_paths()
        if self.file_tables:
            self.error_msgs = []
            [self.access_table(file, tables) for file, tables in file_tables.items()]
            if self.error_msgs:
                self.error_msgs = exceph.exceptions_log_deduplicator(exceptions_log=self.error_msgs)
                self._errors_display(error_msgs=self.error_msgs)
        
        super().__init__(browser=self.browser, profile_root=self.profile_root, profiles=self.profiles,
                         file_tables=self.file_tables, tables=self.tables)
    
    def _errors_display(self, error_msgs: List) -> List:
        """ Adds error messages to the error log without duplication.
        Accepts a collection of error messages and adds them to the error log
        """
        print()
        for error_msg_ in error_msgs:
            try:
                print(f'{error_msg_.strerror}\n\t\t{error_msg_.filename}')
            except AttributeError:
                print(error_msg_)
        print()
    
    def make_paths(self):
        """ Creates the path to different browser profiles.
        """
        pathmaker = BrowserPaths(self.browser, self.profile_root, self.profiles)
        self.paths = pathmaker.profilepaths
    
    def access_table(self, file, tables, non_null_fields=None):
        """ Accepts name of file containing the tables and list of table names and creates corresponding Table objects.
        Accessed via the tables attribute.
        """
        error_msgs = []
        current_batch = [Table(table, path.joinpath(file), self.browser, file, profile, copies_subpath=self.copies_subpath)
                         for profile, path in self.paths.items()
                         for table in tables
                         ]
        for table in current_batch:
            table_yielder, exception_raised = table.make_records_yielder(raise_exceptions=False)  # exception is returned here.
            if exception_raised:
                error_msgs.append(exception_raised)
            else:
                self.tables.append(table)
                try:
                    self.profiles.add(table.profile)
                except AttributeError:
                    self.profiles = set()
                    self.profiles.add(table.profile)
        try:
            self.error_msgs.extend(error_msgs)
        except AttributeError:
            if error_msgs:
                error_msgs = exceph.exceptions_log_deduplicator(exceptions_log=error_msgs)
                self._errors_display(error_msgs=error_msgs)
    
    def access_fields(self, table_fields):
        additional_fields = ('browser', 'profile', 'file', 'table')
        current_table_across_profiles = [table for current_tablename in table_fields
                                         for table in self.tables
                                         if table.table == current_tablename
                                         ]
        for current_table in current_table_across_profiles:
            fields = table_fields[current_table.table]
            selected_fields_records = dict.fromkeys(fields, None)
            selected_fields_records.update({field: current_table[field] for field in additional_fields})
            for record in current_table.records_yielder:
                selected_fields_records.update({field_: record[field_] for field_ in fields})
                # self.selected_fields_records = selected_fields_records
                yield tuple(selected_fields_records.values())
            current_table.make_records_yielder(raise_exceptions=False)
    
    def __repr__(self):
        return f'Browser("{self.browser}", "{self.profile_root}", {self.profiles}, {self.file_tables})'
    
    def __str__(self):
        return f'Browser: {self.browser}, files: {self.files}, profiles: {self.profiles}'


if __name__ == '__main__':  # pragma: no cover
    # test_browser()
    # chrome = Browser(browser='chrome', profile_root='C:\\Users\\kshit\\AppData\\Local\\Google\\Chrome\\User Data')
    
    firefox_auto = Browser(browser='firefox',
                           profile_root='~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles',
                           profiles=['Employment'],
                           file_tables={'places.sqlite': ['moz_places', 'moz_bookmarks'],
                                        'permissions.sqlite': ['moz_hosts']})
    quit()
    firefox_auto.access_fields({'moz_places': ['id', 'url', 'title', 'last_visit_date', 'last_visit_readable']})
    firefox_auto = Browser(browser='firefox',
                           profile_root='~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles',
                           profiles=['test_profile0', 'test_profile1'],
                           file_tables={'places.sqlite': ['moz_places', 'moz_bookmarks'],
                                        'permissions.sqlite': ['moz_hosts']})

# rb.get_tablenames('C:/Users/kshit/AppData/Roaming/Mozilla/Firefox/Profiles/vy2bqplf.dev-edition-default/places.sqlite')


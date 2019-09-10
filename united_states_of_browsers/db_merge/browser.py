# -*- encoding: utf-8 -*-
"""
The Browser class
"""
from collections import namedtuple

from united_states_of_browsers.db_merge import exceptions_handling as exceph
from united_states_of_browsers.db_merge.browserpaths import BrowserPaths
from united_states_of_browsers.db_merge.imported_annotations import *
from united_states_of_browsers.db_merge.table import Table

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
        
        add_tables_for_access(file, tables)

    **Usage:**
        browser_obj = Browser(browser, profile_root, profiles, {database_file1: [table1, table2], database_file2: [table3, table4]})

    Add additional file and tables to existing Browser objects using the add_tables_for_access() method.
            browser_obj.add_tables_for_access(database_file1, [table1, table2])
            
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
        self.available_tables = []
        self.copies_subpath = copies_subpath
        self.make_paths()
        super().__init__(browser=self.browser, profile_root=self.profile_root, profiles=self.profiles,
                         file_tables=self.file_tables, tables=self.available_tables)
    
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
        
    def make_records_yielder(self, filename, tablename, fieldnames=None):
        for profile_name, profile_path in self.paths.items():
            filepath = Path(profile_path, filename)
            profile_name = Path(profile_path).name
            table_obj = Table(table=tablename,
                              path=filepath,
                              browser=self.browser,
                              filename=filename,
                              profile=profile_name,
                              copies_subpath=self.copies_subpath,
                              )
            additional_info = {'browser': self.browser, 'profile': profile_name,
                               'file': filename, 'table': tablename,
                               }
            table_obj.make_records_yielder()
            if fieldnames:
                for record in table_obj.records_yielder:
                    record = {field_name: field_value for
                              field_name, field_value in record.items() if
                              field_name in fieldnames}
                    record.update(additional_info)
                    yield record
            else:
                for record in table_obj.records_yielder:
                    record.update(additional_info)
                    yield record
            
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


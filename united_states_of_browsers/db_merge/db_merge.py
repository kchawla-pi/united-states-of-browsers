# -*- ecnoding: utf-8 -*-
"""
Main file of the United States of Browsers
To create a merged database, run:
	$python db_merge.py
"""
import os
import sqlite3

from united_states_of_browsers.db_merge import browser_data
from united_states_of_browsers.db_merge.browser import (
    make_browser_records_yielder,
    )
from united_states_of_browsers.db_merge.db_search import check_fts5
from united_states_of_browsers.db_merge.helpers import make_queries
from united_states_of_browsers.db_merge.imported_annotations import *


class DatabaseMergeOrchestrator:
    """
    Orchestrates the running of the app, calling the various functions.
    """
    def __init__(self, app_path: PathInfo, db_name: Text, browser_info: BrowserData) -> None:
        try:
            self.app_path = Path(app_path).expanduser()
        except TypeError:
            self.app_path = Path(*app_path).expanduser()
        self.db_name = db_name
        self.browser_info = browser_info
        self.profile_paths = None
        self.browser_yielder = []
        self.output_db = self.app_path.joinpath(db_name)
        self.installed_browsers_data = None
    
    def find_installed_browsers(self):
        """
        Checks if the default browser paths exist on the system to determine if they are installed.
        """
        self.installed_browsers_data = [browser_datum
                                        for browser_datum in self.browser_info
                                        if Path(browser_datum.path).expanduser().absolute().exists()
                                        and browser_datum.os == os.name
                                        ]
    
    def make_records_yielders(self):
        """
        Creates a Browser object for each discovered browser, initializes it with necessary info,
        accesses the specified tables and fields from those Browser objects,
        and creates a generator which will yield records from those tables and fields.
        The generator is stored in:
                DatabaseMergeOrchestrator_obj.browser_yielder
        """
        for browser_datum in self.installed_browsers_data:
            file, _ = tuple(browser_datum.file_tables.items())[0]
            table_name, fields_list = tuple(browser_datum.table_fields.items())[0]

            each_browser_records_yielder = make_browser_records_yielder(
                    browser=browser_datum.browser,
                    profile_root=browser_datum.path,
                    filename=file,
                    tablename=table_name,
                    profiles=browser_datum.profiles,
                    fieldnames=fields_list,
                    copies_subpath=self.app_path,
            )

            self.browser_yielder.append(each_browser_records_yielder)
    
    def rename_existing_db(self):
        """
        If the merged history sqlite database file already exists,
        renames it to prevent it being overwritten by a new database file.
        """
        previous_db_path = self.output_db.with_name('_previous_' + self.output_db.name)
        
        try:
            self.output_db.rename(previous_db_path)
        except FileNotFoundError:
            pass
        except FileExistsError:
            previous_db_path.unlink()
            self.output_db.rename(previous_db_path)
    
    def write_records(self, tablename: Text, primary_key_name: Text, fieldnames: Sequence[Text]):
        """
        Creates a new sqlite database file with te specified table name, primary key name and list of field names.
        :param tablename: Name of the new table.
        :param primary_key_name: Set the name of the primary key field. Must be one of the fieldnames passed in.
        :param fieldnames: List of fieldnames in the new table.
        """
        if ' ' in tablename:  # space in table name malforms the SQL statements.
            raise ValueError(f"Table name cannot have spaces. You provided '{tablename}'")
        queries = make_queries(tablename, primary_key_name, fieldnames)
        with sqlite3.connect(str(self.output_db)) as connection:
            cursor = connection.cursor()
            cursor.execute(queries['create'])
            records_yielder = (tuple(browser_record.values())
                               for browser_record_yielder in
                               self.browser_yielder
                               for browser_record in browser_record_yielder)
            cursor.executemany(queries['insert'], records_yielder)

    def build_search_table(self):
        """
        Builds a virtual search table in the newly created sqlite database file.
        Search table uses fts5 extension of sqlite.
        """
        search_table_fields_str = ", ".join(browser_data.search_table_fields)
        create_virtual_query = f'CREATE VIRTUAL TABLE IF NOT EXISTS search_table USING fts5({search_table_fields_str})'
        read_query = 'SELECT * FROM history WHERE title IS NOT NULL'
        insert_virtual_query = f'INSERT INTO search_table {read_query}'
        with sqlite3.connect(str(self.output_db)) as connection:
            cursor = connection.cursor()
            cursor.execute(create_virtual_query)
            cursor.execute(insert_virtual_query)
    
    def write_db_path_to_file(self, output_dir=None):
        """
        Writes the complete path to the newly created sqlite database
        to a text file in the specified output_dir,
        by default: <UserDir>/AppData/merged_db_path.txt
        """
        output_dir = output_dir if output_dir else Path(__file__).parents[1]
        db_path_store_dir = Path(output_dir, 'AppData')
        db_path_store_dir.mkdir(parents=True, exist_ok=True)
        db_path_store = db_path_store_dir.joinpath('merged_db_path.txt')
        with open(db_path_store, 'w') as file_obj:
            file_obj.write(f'{self.output_db.as_posix()}')

    def orchestrate_db_merge(self):
        """
        Builds the combined database and its search table.
        """
        self.find_installed_browsers()
        self.make_records_yielders()
        '''
        using table as column name seems to conflict with SQL, 
        table_ for example was not giving sqlite3 syntax error on create.
        '''
        self.rename_existing_db()
        self.write_records(tablename='history', primary_key_name='rec_num',
                           fieldnames=browser_data.history_table_fieldnames)
        if check_fts5():
            self.build_search_table()
        else:
            print('FTS5 extension for SQLIte not available/enabled. Search functionality unavailable.')
        self.write_db_path_to_file()


def merge_browsers_history(app_path, merged_db_name):
    all_browsers_info = browser_data.prep_browsers_info()
    write_combi_db = DatabaseMergeOrchestrator(app_path=app_path, db_name=merged_db_name, browser_info=all_browsers_info)
    write_combi_db.orchestrate_db_merge()
# build_search_table('combined_db_fx_cr.sqlite', ['id', 'url', 'title', 'last_visit_time'])

def usb_merge():
    app_path = ('~', 'USB')
    merged_db_name = 'usb_db.sqlite'
    merge_browsers_history(app_path , merged_db_name)


if __name__ == '__main__':
    usb_merge()

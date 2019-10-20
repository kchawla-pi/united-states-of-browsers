# -*- ecnoding: utf-8 -*-
"""
Main file of the United States of Browsers
To create a merged database, run:
	$python db_merge.py
"""
import os
import sqlite3
import warnings

from united_states_of_browsers.db_merge import browser_data
from united_states_of_browsers.db_merge.browser import (
    make_browser_records_yielder,
    )
from united_states_of_browsers.db_merge.helpers import make_queries
from united_states_of_browsers.db_merge.imported_annotations import *


def make_paths(app_path, db_name):
    try:
        app_path = Path(app_path).expanduser()
    except TypeError:
        app_path = Path(*app_path).expanduser()
    app_path.mkdir(parents=True, exist_ok=True)
    output_db = app_path.joinpath(db_name)
    return app_path, output_db


def find_installed_browsers(browser_info):
    """
    Checks if the default browser paths exist on the system to determine if they are installed.
    """
    installed_browsers_data = [browser_datum
                               for browser_datum in browser_info
                               if Path(
            browser_datum.path).expanduser().absolute().exists()
                               and browser_datum.os == os.name
                               ]
    return installed_browsers_data


def make_records_yielders(browsers_data, app_path):
    """
    Creates a Browser object for each discovered browser, initializes it with necessary info,
    accesses the specified tables and fields from those Browser objects,
    and creates a generator which will yield records from those tables and fields.
    The generator is stored in:
            DatabaseMergeOrchestrator_obj.browser_yielder
    """
    browser_yielder = []
    for browser_datum in browsers_data:
        file, _ = tuple(browser_datum.file_tables.items())[0]
        table_name, fields_list = tuple(browser_datum.table_fields.items())[0]

        each_browser_records_yielder = make_browser_records_yielder(
                browser=browser_datum.browser,
                profile_root=browser_datum.path,
                filename=file,
                tablename=table_name,
                profiles=browser_datum.profiles,
                fieldnames=fields_list,
                copies_subpath=app_path,
        )

        browser_yielder.append(each_browser_records_yielder)
    return browser_yielder


def rename_existing_db(output_db):
    """
    If the merged history sqlite database file already exists,
    renames it to prevent it being overwritten by a new database file.
    """
    previous_db_path = output_db.with_name('_previous_' + output_db.name)

    try:
        output_db.rename(previous_db_path)
    except FileNotFoundError:
        pass
    except FileExistsError:
        previous_db_path.unlink()
        output_db.rename(previous_db_path)
    

def write_records(records_yielders, output_db, tablename: Text, primary_key_name: Text, fieldnames: Sequence[Text]):
    """
    Creates a new sqlite database file with te specified table name, primary key name and list of field names.
    :param tablename: Name of the new table.
    :param primary_key_name: Set the name of the primary key field. Must be one of the fieldnames passed in.
    :param fieldnames: List of fieldnames in the new table.
    """
    if ' ' in tablename:  # space in table name malforms the SQL statements.
        raise ValueError(f"Table name cannot have spaces. You provided '{tablename}'")
    queries = make_queries(tablename, primary_key_name, fieldnames)
    with sqlite3.connect(str(output_db)) as connection:
        cursor = connection.cursor()
        cursor.execute(queries['create'])
        records_yielder = (tuple(browser_record.values())
                           for browser_record_yielder in
                           records_yielders
                           for browser_record in browser_record_yielder)
        cursor.executemany(queries['insert'], records_yielder)


def build_search_table(output_db):
    """
    Builds a virtual search table in the newly created sqlite database file.
    Search table uses fts5 extension of sqlite.
    """
    search_table_fields_str = ", ".join(browser_data.search_table_fields)
    create_virtual_query = f'CREATE VIRTUAL TABLE IF NOT EXISTS search_table USING fts5({search_table_fields_str})'
    read_query = 'SELECT * FROM history' # WHERE title IS NOT NULL'
    insert_virtual_query = f'INSERT INTO search_table {read_query}'
    with sqlite3.connect(str(output_db)) as connection:
        cursor = connection.cursor()
        cursor.execute(create_virtual_query)
        cursor.execute(insert_virtual_query)
    

def write_db_path_to_file(output_db, output_dir=None):
    """
    Writes the complete path to the newly created sqlite database
    to a text file in the specified output_dir,
    by default: <UserDir>/AppData/merged_db_path.txt
    """
    output_dir = output_dir if output_dir else Path('~', '.USB').expanduser()
    db_path_store_dir = Path(output_dir, 'AppData')
    db_path_store_dir.mkdir(parents=True, exist_ok=True)
    db_path_store = db_path_store_dir.joinpath('merged_db_path.txt')
    with open(db_path_store, 'w') as file_obj:
        file_obj.write(f'{output_db.as_posix()}')


def orchestrate_db_merge(app_path, db_name, browser_info):
    """
    Builds the combined database and its search table.
    """
    app_path, output_db = make_paths(app_path, db_name)
    installed_browsers_data = find_installed_browsers(
            browser_info=browser_info
            )
    browser_records_yielder = make_records_yielders(
            browsers_data=installed_browsers_data,
            app_path=app_path,
            )
    '''
    using table as column name seems to conflict with SQL, 
    table_ for example was not giving sqlite3 syntax error on create.
    '''
    rename_existing_db(output_db)
    write_records(records_yielders=browser_records_yielder,
                  output_db=output_db,
                  tablename='history',
                  primary_key_name='rec_num',
                  fieldnames=browser_data.history_table_fieldnames,
                  )
    try:
        build_search_table(output_db=output_db)
    except sqlite3.OperationalError as excep:
        if str(excep) == 'no such module: fts5':
            warnings.warn('FTS5 extension for SQLIte not available/enabled. Search functionality unavailable.')
        else:
            raise excep
    write_db_path_to_file(output_db)
    return output_db


def merge_browsers_history(app_path, merged_db_name):  # pragma: no cover
    all_browsers_info = browser_data.prep_browsers_info()
    orchestrate_db_merge(app_path=app_path, db_name=merged_db_name, browser_info=all_browsers_info)


def usb_merge():  # pragma: no cover
    app_path = ('~', '.USB')
    merged_db_name = 'usb_db.sqlite'
    merge_browsers_history(app_path , merged_db_name)


if __name__ == '__main__':  # pragma: no cover
    usb_merge()

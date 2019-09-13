# -*- encoding: utf-8 -*-
"""
The Browser class
"""
from collections import namedtuple

from united_states_of_browsers.db_merge.browserpaths import make_browser_paths
from united_states_of_browsers.db_merge.imported_annotations import *
from united_states_of_browsers.db_merge.table import Table

TableMetadata = namedtuple('TableMetadata', 'browser profile file table')


def make_browser_records_yielder(browser: Text,
                                 profile_root: PathInfo,
                                 filename: Text,
                                 tablename: Text,
                                 profiles: Optional[Iterable[Text]] = None,
                                 fieldnames: Optional[Iterable[Text]] = None,
                                 copies_subpath: Optional[PathInfo] = None
                                 ):
    """ Creates a generator of browser database records.
    Accepts parameters-
        :param: browser: browser name
        :param: profile_root: path to directory/folder where the browser stores all of its profiles
        :param: profiles: list of profile, default is all profiles
        :param: copies_subpath: path where a copy of the database files is created, and read from,instead of the original files.

    """
    paths = make_browser_paths(browser, profile_root, profiles)
    for profile_name, profile_path in paths.items():
        filepath = Path(profile_path, filename)
        profile_name = Path(profile_path).name
        table_obj = Table(table=tablename,
                          path=filepath,
                          browser=browser,
                          filename=filename,
                          profile=profile_name,
                          copies_subpath=copies_subpath,
                          )
        additional_info = {'browser': browser, 'profile': profile_name,
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

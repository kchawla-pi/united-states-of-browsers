# -*- encoding: utf-8 -*-
"""
The Browser class
"""
from collections import namedtuple

from united_states_of_browsers.db_merge.browserpaths import BrowserPaths
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
    paths = BrowserPaths(browser, profile_root, profiles).profilepaths
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


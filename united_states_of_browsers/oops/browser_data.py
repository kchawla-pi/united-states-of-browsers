from collections import namedtuple


BrowserData = namedtuple('BrowserData', 'os browser path profiles file_tables table_fields')

all_browsers = [BrowserData(os='nt',
                            browser='firefox',
                            path='~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles',
                            profiles=None,
                            file_tables={'places.sqlite': ['moz_places']},
                            table_fields={'moz_places': ['id', 'url', 'title', 'last_visit_date', 'last_visit_readable']},
                            ),
                BrowserData(os='nt',
                            browser='chrome',
                            path='~\\AppData\\Local\\Google\\Chrome\\User Data',
                            profiles=None,
                            file_tables={'history': ['urls']},
                            table_fields={'urls': ['id', 'url', 'title', 'last_visit_time', 'last_visit_readable']},
                            ),
                BrowserData(os='nt',
                            browser='opera',
                            path='~\\AppData\\Roaming\\Opera Software',
                            profiles=None,
                            file_tables={'History': ['urls']},
                            table_fields={'urls': ['id', 'url', 'title', 'last_visit_time', 'last_visit_readable']},
                            ),
                BrowserData(os='nt',
                            browser='vivaldi',
                            path='~\\AppData\\Local\\Vivaldi\\User Data',
                            profiles=None,
                            file_tables={'History': ['urls']},
                            table_fields={'urls': ['id', 'url', 'title', 'last_visit_time', 'last_visit_readable']},
                            ),
                ]

history_table_fieldnames = ['id', 'url', 'title', 'last_visit', 'last_visit_readable', 'browser', 'profile', 'file', 'tablename']
search_table_fields = ['rec_id', 'id', 'url', 'title', 'last_visit', 'last_visit_readable', 'browser', 'profile', 'file',
		                 'tablename']

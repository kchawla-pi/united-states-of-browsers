from united_states_of_browsers.db_merge import (db_search,
                                                merge_browser_databases
                                                )

merge_browser_databases.merge_records(output_db='all_merged', profiles=None, table='moz_places')
# # db_search.build_search_table()

"""
from io import BytesIO
from zipfile import ZipFile
import requests

def get_zip(file_url):
    url = requests.get(file_url)
    zipfile = ZipFile(BytesIO(url.content))
    zip_names = zipfile.namelist()
    if len(zip_names) == 1:
        file_name = zip_names.pop()
        extracted_file = zipfile.open(file_name)
        return extracted_file
"""

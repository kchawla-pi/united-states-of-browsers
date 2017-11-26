# from united_states_of_browsers.db_merge import (db_search,
#                                                 merge_browser_databases
#                                                 )

# merge_browser_databases.merge_records(output_db='all_merged', profiles=None, table='moz_places')

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
import os
import venv

from pprint import pprint


pprint(os.environ['VIRTUAL_ENV'])
# virt_env = venv.EnvBuilder()
# virt_env.create('venv')
# virt_env.post_setup(virt_env.)

class CustomEnvBuilder(venv.EnvBuilder):
	def __init__(self, env_dir, packages=list()):
		pass
		super().__init___(env_dir)
	def post_setup(self, context):
		""" Sets up the packages required to be pre-installed into the virtual environment
		being created.
		"""
		pass

	def install_package(self):
		pass

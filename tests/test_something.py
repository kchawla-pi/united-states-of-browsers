from pathlib import Path
import sys


search_path = str(Path(__file__).parents[1])
sys.path.insert(0, search_path)

import united_states_of_browsers
from united_states_of_browsers import db_merge

def test_mock():
	return print(True)


test_mock()
db_merge.browser_setup.db_filepath()

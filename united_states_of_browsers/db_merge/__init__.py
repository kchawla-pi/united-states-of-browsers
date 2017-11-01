import pathlib
import sys

search_in = pathlib.Path(__file__).parent
sys.path.insert(0, str(search_in))

from united_states_of_browsers import db_merge

from . import browser_setup
from . import read_browser_db
from . import imported_annotations
from . import merge_browser_databases

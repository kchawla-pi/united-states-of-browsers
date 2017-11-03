import pathlib
import sys

search_in = pathlib.Path(__file__).parent
sys.path.insert(0, str(search_in))

from united_states_of_browsers import db_merge

from . import browser_specific_setup
from . import db_search
from . import paths_setup
from . import imported_annotations
from . import merge_browser_databases

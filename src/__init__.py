import pathlib
search_in = pathlib.Path(__file__).parent

from . import browser_setup
from . import db_handler
from . import deduplicator
from . import read_browser_db
from . import record_fetcher
from . import write_new_db
from .write_new_db import safetychecks

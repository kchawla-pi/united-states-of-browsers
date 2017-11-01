import pathlib
import sys

search_in = pathlib.Path(__file__).parent
sys.path.insert(0, str(search_in))

from united_states_of_browsers import db_merge

from . import browser_setup
# from . import db_handler
# from . import deduplicator
from . import read_browser_db
# from . import record_fetcher
from . import write_new_db
from . import imported_annotations
from . import merge_browser_databases
# from .write_new_db import safetychecks


# try:
# 	from . import browser_setup
# 	from . import db_handler
# 	# from . import deduplicator
# 	from . import read_browser_db
# 	from . import record_fetcher
# 	from . import write_new_db
# 	from . import imported_annotations
# 	# from .write_new_db import safetychecks
# except (ImportError, ModuleNotFoundError):
# 	from united_states_of_browsers.db_merge_v1 import browser_setup
# 	from united_states_of_browsers.db_merge_v1 import db_handler
# 	# from united_states_of_browsers.db_merge_v1 import deduplicator
# 	from united_states_of_browsers.db_merge_v1 import read_browser_db
# 	from united_states_of_browsers.db_merge_v1 import record_fetcher
# 	from united_states_of_browsers.db_merge_v1 import write_new_db
# 	from united_states_of_browsers.db_merge_v1 import imported_annotations

#
# modules = {
# 'browser_setup': browser_setup,
# 'db_handler': db_handler,
# 'deduplicator': deduplicator,
# 'read_browser_db': read_browser_db,
# 'record_fetcher': record_fetcher,
# 'write_new_db': write_new_db,
# 'imported_annotations': imported_annotations,
# 	}
# for module_ in  modules:
# 	from . import modules[module_]
#

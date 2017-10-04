import sqlite3

import browser_setup
import read_browser_db

# db_paths = browser_setup.setup_profile_paths(browser_ref='firefox', profiles=None)
db_paths = read_browser_db.firefox()
# prepped_records = read_browser_database.read_browser_database(db_paths)



print(db_paths)

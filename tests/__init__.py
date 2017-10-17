from pathlib import Path
import sys


search_path = str(Path(__file__).parents[1])
sys.path.insert(0, search_path)


from united_states_of_browsers import db_merge, usb_server

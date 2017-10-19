import pytest

from united_states_of_browsers.db_merge import browser_setup

print(browser_setup.setup_profile_paths(browser_ref='firefox', profiles=None))

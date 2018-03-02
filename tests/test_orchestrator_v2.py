from pathlib import Path

from united_states_of_browsers.db_merge.orchestrator import Orchestrator
from united_states_of_browsers.db_merge.browser_data import prep_browsers_info

app_path = '~/USB/for_tests'
db_name = 'test.sqlite'
new_parent = Path(__file__).parents[1].joinpath('tests', 'data', 'browser_profiles_for_testing')

browser_info = prep_browsers_info(parent_dir=new_parent)
test_orchestrator = Orchestrator(app_path=app_path, db_name=db_name, browser_info=browser_info)
test_orchestrator.orchestrate()
print()

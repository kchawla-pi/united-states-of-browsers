import pytest

from src import browser_setup as bs


def test_setup_profile_paths():

	test_inputs = {
		0: ('firefox', 'default'),
		
		1: ('firefox', 'RegularSurfing'),
		2: ('firefox', 'dev-edition-default'),
		3: ('firefox', 'default'),
		
		4: ('~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\px2kvmlk.RegularSurfing', None),
		5: ('~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\vy2bqplf.dev-edition-default', None),
		6: ('~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\xl8257ca.default', None),
		}
	
	expected_outputs = {
		0: {'default': 'C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\xl8257ca.default'},
		
		1: {'RegularSurfing': 'C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\px2kvmlk.RegularSurfing'},
		2: {'dev-edition-default': 'C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\vy2bqplf.dev-edition-default'},
		3: {'default': 'C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\xl8257ca.default'},
		
		4: {'RegularSurfing': 'C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\px2kvmlk.RegularSurfing'},
		5: {'dev-edition-default': 'C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\vy2bqplf.dev-edition-default'},
		6: {'default': 'C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\xl8257ca.default'},
		}
	
	for test_case in range(0, len(test_inputs)):
		browser_name_or_path, profiles = test_inputs[test_case]
		returned = bs.setup_profile_paths(browser_ref=browser_name_or_path, profiles=profiles)
		expected = expected_outputs[test_case]
		
		assert expected == returned


def test_choose_browser_paths():
	
	test_inputs = {
		0: 'firefox',
		1: 'C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles',
		}

	expected_outputs = {
		0: 'C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles',
		1: 'C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles',
		}

	for test_case in range(0, len(test_inputs)):
		returned= bs._choose_browser_paths(browser_ref=test_inputs[test_case])
		expected = expected_outputs[test_case]
		assert expected == returned
		
		
	
	
if __name__ == '__main__':
	pytest.main()

from collections import namedtuple
from pathlib import Path, WindowsPath

from pytest import raises

InputForTesting = namedtuple('InputForTesting', 'browser_ref profiles')

home_dir = Path.home()
setup_profile_paths = {
	InputForTesting(browser_ref='firefox', profiles=None):
		{
		'RegularSurfing': Path(f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/px2kvmlk.RegularSurfing'),
		'default': Path(f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/xl8257ca.default'),
		'dev-edition-default': Path(f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/vy2bqplf.dev-edition-default'),
		'kc.qubit': Path(f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/qllr6o0m.kc.qubit'),
		'test_profile0': Path(f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/e0pj4lec.test_profile0'),
		'test_profile1': Path(f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/kceyj748.test_profile1'),
		'test_profile2': Path(f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/udd5sttq.test_profile2')
		},
	
	InputForTesting(browser_ref='firefox', profiles='RegularSurfing'):
		{
		'RegularSurfing': Path(f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/px2kvmlk.RegularSurfing'),
		},

	InputForTesting(browser_ref='', profiles=''):
		{},
	
	InputForTesting(browser_ref='somegibberish', profiles='somemoregibberish'):
		"[WinError 3] The system cannot find the path specified: 'somegibberish'",
	
	InputForTesting(browser_ref=123, profiles=321):
		"expected str, bytes or os.PathLike object, not int",
	
	InputForTesting(browser_ref=123.123, profiles=321.321):
		"expected str, bytes or os.PathLike object, not float",
	
	InputForTesting(browser_ref='rubbishpath', profiles=None):
		"[WinError 3] The system cannot find the path specified: 'rubbishpath'",
	
	InputForTesting(browser_ref='C:\\Users\\default\\Desktop', profiles=None):
		{},
	
	InputForTesting(browser_ref=Path(f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles'),
	                profiles=None):
		{
			'RegularSurfing': Path(
					f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/px2kvmlk.RegularSurfing'),
			'default': Path(
					f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/xl8257ca.default'),
			'dev-edition-default': Path(
					f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/vy2bqplf.dev-edition-default'),
			'kc.qubit': Path(
					f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/qllr6o0m.kc.qubit'),
			'test_profile0': Path(
					f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/e0pj4lec.test_profile0'),
			'test_profile1': Path(
					f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/kceyj748.test_profile1'),
			'test_profile2': Path(
					f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/udd5sttq.test_profile2')
		},
	
	InputForTesting(browser_ref='Firefox', profiles=None): # 'Firefox' instead of 'firefox'
		"[WinError 3] The system cannot find the path specified: 'Firefox'",
	
	InputForTesting(browser_ref='firefox',
	                profiles=('regular_surfing', 'default', None, 'programming')):
		{
			'default': Path(f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/xl8257ca.default')
		},
	
	InputForTesting(browser_ref='firefox',
	                profiles=('regular_surfing', 'default', None, 'programming')):
		{
			'default': Path(f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/xl8257ca.default')
		},
		
	}

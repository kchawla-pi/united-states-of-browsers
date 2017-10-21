import types

from collections import namedtuple
from pathlib import Path


home_dir = Path.home()

def data_for_setup_profile_paths():
	TestCase = namedtuple('TestCase', 'browser_ref profiles expected')
	setup_profile_paths = (
		TestCase(browser_ref='firefox', profiles=None,
		         expected=
			{
			'RegularSurfing': Path(f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/px2kvmlk.RegularSurfing'),
			'default': Path(f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/xl8257ca.default'),
			'dev-edition-default': Path(f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/vy2bqplf.dev-edition-default'),
			'kc.qubit': Path(f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/qllr6o0m.kc.qubit'),
			'test_profile0': Path(f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/e0pj4lec.test_profile0'),
			'test_profile1': Path(f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/kceyj748.test_profile1'),
			'test_profile2': Path(f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/udd5sttq.test_profile2')
			}
		         ),
		
		TestCase(browser_ref='firefox', profiles='RegularSurfing',
		         expected={
			         'RegularSurfing': Path(f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/px2kvmlk.RegularSurfing'),
			         }
		         ),
	
		TestCase(browser_ref='', profiles='',
		         expected={}
		         ),
		
		TestCase(browser_ref='somegibberish', profiles='somemoregibberish',
		         expected="[WinError 3] The system cannot find the path specified: 'somegibberish'"
		         ),
		
		TestCase(browser_ref=123, profiles=321,
		         expected="expected str, bytes or os.PathLike object, not int"
		         ),
		
		TestCase(browser_ref=123.123, profiles=321.321,
		         expected="expected str, bytes or os.PathLike object, not float"
		         ),
		
		TestCase(browser_ref='rubbishpath', profiles=None,
		         expected="[WinError 3] The system cannot find the path specified: 'rubbishpath'"
		         ),
		
		TestCase(browser_ref='C:\\Users\\default\\Desktop', profiles=None,
		         expected={}
		         ),
		
		TestCase(browser_ref=Path(f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles'),
		                profiles=None,
		         expected={
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
			         }
		         ),
		
		TestCase(browser_ref='Firefox', profiles=None, # 'Firefox' instead of 'firefox'
		         expected="[WinError 3] The system cannot find the path specified: 'Firefox'"
		         ),
		
		TestCase(browser_ref='firefox',
		         profiles=('regular_surfing', 'default', None, 'programming'),
		         expected={'default':
			                   Path(f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/xl8257ca.default')
		                   }
		         ),
		
		TestCase(browser_ref='firefox',
		         profiles=('regular_surfing', 'default', None, 'programming'),
		         expected={'default':
			                   Path(f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/xl8257ca.default')
		                   }
		         ),
		
		)
	return setup_profile_paths


setup_profile_paths = data_for_setup_profile_paths()

"""
def data_for_db_filepaths():
	InputForTesting = namedtuple('InputForTesting', 'profilepaths files ext')
	db_filepaths = {
		InputForTesting(files=None, ext='sqlite',
		                profilepaths=types.MappingProxyType({
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
			                })
		                ):
			{},
		}
	
	return db_filepaths

db_filepaths = data_for_db_filepaths()
"""

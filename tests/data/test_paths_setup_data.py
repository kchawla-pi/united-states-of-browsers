from collections import namedtuple
from pathlib import Path


home_dir = Path.home()


def data_for_setup_profile_paths():
	setup_profile_paths_testdata = dict.fromkeys(['values', 'exceps'])
	TestCase = namedtuple('TestCase', 'browser_ref profiles expected')
	
	setup_profile_paths_testdata['values'] = (
		TestCase(browser_ref='firefox', profiles=None,
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
		TestCase(browser_ref='firefox', profiles='RegularSurfing',
		         expected={
			         'RegularSurfing': Path(
					         f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/px2kvmlk.RegularSurfing'),
			         }
		         ),
		TestCase(browser_ref='', profiles='',
		         expected={}
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
		TestCase(browser_ref='firefox',
		         profiles=('regular_surfing', 'default', None, 'programming'),
		         expected={'default':
			         Path(
					         f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/xl8257ca.default')
			         }
		         ),
		TestCase(browser_ref='firefox',
		         profiles=('regular_surfing', 'default', None, 'programming'),
		         expected={'default':
			         Path(
					         f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/xl8257ca.default')
			         }
		         ),
		)
	
	setup_profile_paths_testdata['exceps'] = (
		TestCase(browser_ref='somegibberish', profiles='somemoregibberish',
		         expected=FileNotFoundError
		         ),
		TestCase(browser_ref=123, profiles=321,
		         expected=TypeError
		         ),
		TestCase(browser_ref=123.123, profiles=321.321,
		         expected=TypeError
		         ),
		TestCase(browser_ref='rubbishpath', profiles=None,
		         expected=FileNotFoundError
		         ),
		TestCase(browser_ref='Firefox', profiles=None, # 'Firefox' instead of 'firefox'
		         expected=FileNotFoundError
		         ),
		)
	
	return setup_profile_paths_testdata


setup_profile_paths_testdata = data_for_setup_profile_paths()


# """
def data_for_db_filepaths():
	db_filepaths_testdata = dict.fromkeys(['defaults', 'values', 'exceps'])
	TestCase = namedtuple('TestCase', 'profile_paths filenames ext expected')
	TestCaseDefault = namedtuple('TestCaseDefault', 'profile_paths expected')
	
	db_filepaths_testdata['defaults'] = (
		TestCaseDefault(
				profile_paths={
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
							f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/udd5sttq.test_profile2'),
					},
				expected={
					'RegularSurfing':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\px2kvmlk.RegularSurfing\\places.sqlite',
					'default':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\xl8257ca.default\\places.sqlite',
					'dev-edition-default':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\vy2bqplf.dev-edition-default\\places.sqlite',
					'kc.qubit':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\qllr6o0m.kc.qubit\\places.sqlite',
					'test_profile0':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\e0pj4lec.test_profile0\\places.sqlite',
					'test_profile1':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\kceyj748.test_profile1\\places.sqlite',
					'test_profile2':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\udd5sttq.test_profile2\\places.sqlite',
					}
				),
		TestCaseDefault(
				profile_paths={'RegularSurfing':
					Path(
							f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/px2kvmlk.RegularSurfing')
					},
				expected={'RegularSurfing':
					          f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\px2kvmlk.RegularSurfing\\places.sqlite'
				          }
				),
		)
	
	db_filepaths_testdata['values'] = (
		TestCase(
				profile_paths={
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
							f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/udd5sttq.test_profile2'),
					},
				filenames='places', ext='sqlite',
				expected={
					'RegularSurfing':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\px2kvmlk.RegularSurfing\\places.sqlite',
					'default':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\xl8257ca.default\\places.sqlite',
					'dev-edition-default':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\vy2bqplf.dev-edition-default\\places.sqlite',
					'kc.qubit':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\qllr6o0m.kc.qubit\\places.sqlite',
					'test_profile0':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\e0pj4lec.test_profile0\\places.sqlite',
					'test_profile1':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\kceyj748.test_profile1\\places.sqlite',
					'test_profile2':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\udd5sttq.test_profile2\\places.sqlite',
					}
				),
		TestCase(
				profile_paths={
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
							f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/udd5sttq.test_profile2'),
					},
				filenames='somegibberish', ext='sqlite',
				expected={
					'RegularSurfing':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\px2kvmlk.RegularSurfing\\somegibberish.sqlite',
					'default':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\xl8257ca.default\\somegibberish.sqlite',
					'dev-edition-default':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\vy2bqplf.dev-edition-default\\somegibberish.sqlite',
					'kc.qubit':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\qllr6o0m.kc.qubit\\somegibberish.sqlite',
					'test_profile0':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\e0pj4lec.test_profile0\\somegibberish.sqlite',
					'test_profile1':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\kceyj748.test_profile1\\somegibberish.sqlite',
					'test_profile2':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\udd5sttq.test_profile2\\somegibberish.sqlite',
					}
				),
		TestCase(
				profile_paths={
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
							f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/udd5sttq.test_profile2'),
					},
				filenames='places', ext='gibberishext',
				expected={
					'RegularSurfing':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\px2kvmlk.RegularSurfing\\places.gibberishext',
					'default':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\xl8257ca.default\\places.gibberishext',
					'dev-edition-default':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\vy2bqplf.dev-edition-default\\places.gibberishext',
					'kc.qubit':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\qllr6o0m.kc.qubit\\places.gibberishext',
					'test_profile0':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\e0pj4lec.test_profile0\\places.gibberishext',
					'test_profile1':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\kceyj748.test_profile1\\places.gibberishext',
					'test_profile2':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\udd5sttq.test_profile2\\places.gibberishext',
					}
				),
		TestCase(
				profile_paths={
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
							f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/udd5sttq.test_profile2'),
					},
				filenames='', ext='.sqlite',
				expected={
					'RegularSurfing':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\px2kvmlk.RegularSurfing\\.sqlite',
					'default':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\xl8257ca.default\\.sqlite',
					'dev-edition-default':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\vy2bqplf.dev-edition-default\\.sqlite',
					'kc.qubit':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\qllr6o0m.kc.qubit\\.sqlite',
					'test_profile0':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\e0pj4lec.test_profile0\\.sqlite',
					'test_profile1':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\kceyj748.test_profile1\\.sqlite',
					'test_profile2':
						f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\udd5sttq.test_profile2\\.sqlite',
					}
				),
		TestCase(
				profile_paths={'RegularSurfing':
					Path(
							f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/px2kvmlk.RegularSurfing')
					},
				filenames='places', ext='sqlite',
				expected={'RegularSurfing':
					          f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\px2kvmlk.RegularSurfing\\places.sqlite'
				          }
				),
		TestCase(
				profile_paths={'someprofile': 'gibberish'},
				filenames='places', ext='sqlite',
				expected={'someprofile': 'gibberish\\places.sqlite'}
				),
		)
	
	db_filepaths_testdata['exceps'] = (
		TestCase(
				profile_paths={
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
							f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/udd5sttq.test_profile2'),
					},
				filenames=None, ext='sqlite',
				expected=TypeError
				),
		TestCase(
				profile_paths={
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
							f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/udd5sttq.test_profile2'),
					},
				filenames=[None], ext='sqlite',
				expected=TypeError
				),
		TestCase(
				profile_paths=123,
				filenames='places', ext='sqlite',
				expected=AttributeError
				),
		TestCase(
				profile_paths={
					f'{home_dir}/AppData/Roaming/Mozilla/Firefox/Profiles/px2kvmlk.RegularSurfing'},
				filenames='places', ext='sqlite',
				expected=AttributeError
				),
		TestCase(
				profile_paths=123,
				filenames='places', ext='sqlite',
				expected=AttributeError
				),
		)
	
	return db_filepaths_testdata


db_filepaths_testdata = data_for_db_filepaths()
# """

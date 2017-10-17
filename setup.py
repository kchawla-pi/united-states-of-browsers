import setuptools

from pathlib import Path



# Path(__file__).parents
setuptools.setup(
		name='usb',
		version='0.2dev',
		packages=setuptools.find_packages('united_states_of_browsers'),
		packages_dir={'':'united_states_of_browsers'},
		
		author='kchawla-pi',
		author_email='kc.insight.pi@gmail.com',
		description='Manage and search browser histories across multiple browsers and browser profiles.',
		long_description=open('README.md').read(),
		keywords='browser history',
		url='https://github.com/kchawla-pi/united-states-of-browsers',
		)
		
		

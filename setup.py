import setuptools

from pathlib import Path


setuptools.setup(
        name='usb',
        version='0.0.83.dev0',
        packages=['tests',
                  'united_states_of_browsers',
                  'united_states_of_browsers.db_merge',
                  'united_states_of_browsers.usb_server'
                  ],
        
        author='kchawla-pi',
        author_email='kc.insight.pi@gmail.com',
        description='Manage and search browser histories across multiple browsers and browser profiles.',
        long_description_content_type="text/markdown",
        long_description=Path('README.md').read_text(),
        keywords='browser history',
        url='https://github.com/kchawla-pi/united-states-of-browsers',
        )

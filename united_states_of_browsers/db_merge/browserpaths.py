# -*- encoding: utf-8 -*-
"""
Module containing classes to setup browser profile paths and database file paths.

Classes: BrowserPaths
"""
from pathlib import Path

from united_states_of_browsers.db_merge import exceptions_handling
from united_states_of_browsers.db_merge.imported_annotations import *


class BrowserPaths(dict):
    """	Creates objects to create paths to browser profile and database files.
    Accepts browser name, browser profiles directory path, database files list, browser profiles list (default: all).

    """
    def __init__(self, browser: Text, profile_root: PathInfo, profiles: Optional[Iterable[Text]]=None):
        self.browser = browser
        self.profile_root = Path(profile_root).expanduser()
        self.profiles = profiles
        self.profilepaths = None
        self.filepaths = None
        self.make_paths()
        super().__init__(browser=browser, profile_root=self.profile_root, profiles=profiles, profilepaths=self.profilepaths,
                         filepaths=self.filepaths
                         )
    
    def _make_firefox_profile_paths(self):
        get_profile_name = lambda dir_entry: str(dir_entry).split(sep='.', maxsplit=1)[1]
        if self.profiles:
            self.profilepaths = {profile: entry for entry in self.profile_root.iterdir()
                                 for profile in self.profiles
                                 if '.' in entry.name and entry.is_dir() and entry.name.endswith(profile)
                                 }
        else:
            self.profilepaths = {get_profile_name(entry): entry
                                 for entry in self.profile_root.iterdir()
                                 if '.' in entry.name and entry.is_dir()}
    
    def _make_chrome_profile_paths(self):
        if self.profiles:
            self.profilepaths = {entry.name: entry
                                 for profile_name in self.profiles
                                 for entry in self.profile_root.iterdir()
                                 if entry.name.endswith(profile_name)}
        else:
            self.profilepaths = {entry.name: entry for entry in self.profile_root.iterdir()
                                 if entry.name.startswith('Profile') or entry.name == 'Default'}
    
    def make_paths(self):
        make_path_chooser = {'firefox': self._make_firefox_profile_paths, 'chrome': self._make_chrome_profile_paths,
                             'opera': self._make_chrome_profile_paths, 'vivaldi': self._make_chrome_profile_paths,
                             }
        try:
            make_path_chooser[self.browser]()
        except FileNotFoundError as excep:
            invalid_path = exceptions_handling.invalid_path_in_tree(excep.filename)
            print(f'In {excep.filename},\npath {invalid_path} does not exist.\nMoving on...')
    
    def __repr__(self):
        if self.profiles:
            return f'BrowserPaths({self.browser}, {self.profile_root}, {self.profiles})'
        else:
            return f'BrowserPaths({self.browser}, {self.profile_root})'

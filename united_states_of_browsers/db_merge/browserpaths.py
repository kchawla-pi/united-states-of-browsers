# -*- encoding: utf-8 -*-
"""
Module containing classes to setup browser profile paths and database file paths.

Classes: BrowserPaths
"""
from pathlib import Path

from united_states_of_browsers.db_merge import exceptions_handling
from united_states_of_browsers.db_merge.imported_annotations import *


"""	Creates objects to create paths to browser profile and database files.
Accepts browser name, browser profiles directory path, database files list, browser profiles list (default: all).

"""
def _make_firefox_profile_paths(profile_root, profiles):
    get_profile_name = lambda dir_entry: str(dir_entry).split(sep='.', maxsplit=1)[1]
    if profiles:
        profilepaths = {profile: entry for entry in profile_root.iterdir()
                             for profile in profiles
                             if '.' in entry.name and entry.is_dir() and entry.name.endswith(profile)
                             }
    else:
        profilepaths = {get_profile_name(entry): entry
                             for entry in profile_root.iterdir()
                             if '.' in entry.name and entry.is_dir()}
    return profilepaths


def _make_chrome_profile_paths(profile_root, profiles):
    if profiles:
        profilepaths = {entry.name: entry
                             for profile_name in profiles
                             for entry in profile_root.iterdir()
                             if entry.name.endswith(profile_name)}
    else:
        profilepaths = {entry.name: entry for entry in profile_root.iterdir()
                             if entry.name.startswith('Profile') or entry.name == 'Default'}
    return profilepaths


def make_browser_paths(browser, profile_root, profiles=None):
    make_path_chooser = {'firefox': _make_firefox_profile_paths, 'chrome': _make_chrome_profile_paths,
                         'opera': _make_chrome_profile_paths, 'vivaldi': _make_chrome_profile_paths,
                         }
    try:
        profilepaths = make_path_chooser[browser](profile_root, profiles)
    except FileNotFoundError as excep:
        invalid_path = exceptions_handling.invalid_path_in_tree(excep.filename)
        print(f'In {excep.filename},\npath {invalid_path} does not exist.\nMoving on...')
        raise excep
    else:
        return profilepaths

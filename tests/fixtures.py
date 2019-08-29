import pytest

from united_states_of_browsers.db_merge import helpers


def get_project_root_path():
    project_dirnames = ['UnitedStatesOfBrowsers',
                        'united-states-of-browsers',
                        ]
    for dirname in project_dirnames:
        try:
            project_root = helpers.get_root_path(
                    project_file_path=__file__,
                    project_root_dir_name=dirname,
                    )
        except ValueError:
            pass
        else:
            break
    else:
        raise ValueError(
                f'Project directory name not in list {project_dirnames}'
                )
    return project_root

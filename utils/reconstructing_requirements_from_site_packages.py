import shutil
import venv

from pathlib import Path
from pprint import pprint

class NewEnvSetup(venv.EnvBuilder):
    def __init__(self):
        super().__init__()


def get_packages_info(site_packages_path):
    suffixes = ('.dist-info', '.egg-info')
    py_packages_name_ver = [entry.stem.split(sep='-')[:2]
                            for entry in site_packages_path.iterdir()
                            for suffix_ in suffixes
                            if str(entry).endswith(suffix_)
                            ]
    return py_packages_name_ver


def backup_origianls(venv_backup_path, site_packages_path, orig_requirements_file):
    venv_backup_path.mkdir()
    shutil.move(site_packages_path, venv_backup_path)
    shutil.move(orig_requirements_file, venv_backup_path)
    
    
def create_new(packages_info, env_dir='venv'):
    requirements = ['=='.join(entry) for entry in packages_info]
    Path('./requirements.txt').write_text('\n'.join(requirements))
    venv.create(env_dir, with_pip=True, symlinks=True)
    # venv.EnvBuilder
    
    
def replace_env(env_dir='venv',
                prompt=None,
                rootpath='.',
                site_packages_path=None,
                new_requirements_file='requirements.txt',
                existing_requirments_file='requirements.txt',
                ):
    if not site_packages_path:
        site_packages_path = Path('./venv/Lib/site-packages')

    
    prompt = prompt if prompt else str(Path(env_dir).stem)

    existing_requirments_file = Path(existing_requirments_file)
    existing_requirments_file = existing_requirments_file if existing_requirments_file.exists() else None
    
    venv_backup_path = Path('./_venv_old')
    packages_info = get_packages_info(site_packages_path)
    backup_origianls(venv_backup_path, site_packages_path,     existing_requirments_file)
    create_new(packages_info, env_dir=env_dir, prompt=prompt)

if __name__ == '__main__':

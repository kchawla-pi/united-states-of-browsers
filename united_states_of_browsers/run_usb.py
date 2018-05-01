import os
import subprocess
import webbrowser

from pathlib import Path


def make_paths():
	venv_python_path = Path(__file__).absolute().parents[1]
	venv_python_path = venv_python_path.joinpath('venv', 'Scripts', 'python.exe')
	run_usb_path = Path(__file__).absolute().parent
	return venv_python_path, run_usb_path
	
	
def make_command_module(venv_python_path, run_usb_path, module_to_be_imported, function_to_be_run):
	launch_command = f'{venv_python_path} -m {run_usb_path}'
	
	
def make_command(venv_python_path, run_usb_path, module_to_be_imported, function_to_be_run):
	launch_command = ' '.join(
			[str(venv_python_path), '-c',
			 f'"import {module_to_be_imported}; {module_to_be_imported}.{function_to_be_run}()"'])
	return launch_command

def launch_usb_mock():
	print('launched')
	quit()
	
	
# def merge_browsers():
# 	from united_states_of_browsers.db_merge.orchestrator import merge_browsers
# 	print('Merging browser databases...')
# 	merge_browsers()
#
# def run_flask():
# 	from united_states_of_browsers.usb_server.usb_server import run_flask
# 	print('Starting browser interface...')
# 	run_flask()
# 	usb_flask_url = 'http://127.0.0.1:5000/'
# 	webbrowser.open_new_tab(url=usb_flask_url)

#
# def launch_usb():
# 	merge_browsers()
# 	run_flask()

def main():
	venv_python_path, run_usb_path = make_paths()
	launch_browser_merge = make_command_module(venv_python_path,
	                                    run_usb_path,
	                                    module_to_be_imported='run_usb',
	                                    function_to_be_run='merge_browsers',
	                                    )
	print(locals())
	
	
	
	
	# launch_ui = make_command(venv_python_path,
	#                          run_usb_path,
	#                          module_to_be_imported='run_usb',
	#                          function_to_be_run='run_flask',
	#                          )
	# curr_dir = os.getcwd()
	# os.chdir(run_usb_path)
	# subprocess.run(launch_browser_merge)
	# subprocess.run(launch_ui)
	# os.chdir(curr_dir)


if __name__ == '__main__':
	main()
	# venv_python_path, run_usb_path = make_paths()
	# curr_dir = os.getcwd()
	# os.chdir(run_usb_path)
	# subprocess.run('C:\\Users\\kshit\\OneDrive\\workspace\\UnitedStatesOfBrowsers\\venv\\Scripts\\python.exe -c '
	#                '"import run_usb; run_usb.launch_usb()"',
	#                )

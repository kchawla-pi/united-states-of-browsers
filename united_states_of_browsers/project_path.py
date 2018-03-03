from pathlib import Path


def get_project_root_path(project_dir):
	project_root_path_parts = Path(__file__).parts
	project_root_dir_idx = project_root_path_parts.index(project_dir)
	project_root = Path(*project_root_path_parts[:project_root_dir_idx+1])
	return project_root

import shutil

from pathlib import Path


class TempFile:
	def __init__(self, filepath, temp_dir=None):
		self.filepath = Path(filepath)
		self.temp_dir = Path(temp_dir) if temp_dir else Path.cwd()

	def copy_file(self):
		shutil.copy2(self.filepath, self.temp_dir)




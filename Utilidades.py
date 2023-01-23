import os
import shutil
from datetime import datetime


def format_package_name(file_name) -> object:
    now = datetime.now()
    return file_name + "_" + str(now.strftime("%Y%m%d_%H%M%S"))


def move_files(self):
    src_files = os.listdir(self.src_dir)
    # create destination directory if it does not exist
    if not os.path.exists(self.dest_dir):
        os.makedirs(self.dest_dir)
    for file_name in src_files:
        full_file_name = os.path.join(self.src_dir, file_name)
        if os.path.isfile(full_file_name):
            shutil.move(full_file_name, self.dest_dir)

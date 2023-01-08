import os
import subprocess

def check_binary_exists(binary):
    try:
        subprocess.check_output(["which", binary])
        return True
    except subprocess.CalledProcessError:
        return False

def check_folders(home_dir, data_dir):
    in_data_dirs = ['weights', 'scratch', 'images', 'logs']
    in_home_dirs = ['hf']
    for in_data_dir in in_data_dirs:
        if not os.path.exists(os.path.join(data_dir, in_data_dir)):
            os.makedirs(os.path.join(data_dir, in_data_dir))
    for in_home_dir in in_home_dirs:
        if not os.path.exists(os.path.join(home_dir, in_home_dir)):
            os.makedirs(os.path.join(home_dir, in_home_dir))
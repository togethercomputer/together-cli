import os
import fcntl
import signal
import subprocess
from loguru import logger
from contextlib import contextmanager
from pynvml import nvmlInit, nvmlDeviceGetCount, nvmlDeviceGetHandleByIndex, nvmlDeviceGetMemoryInfo

try:
    nvmlInit()
except:
    logger.warning("Unable to initialize NVML, GPU information will not be available.")

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

@contextmanager
def timeout(seconds):
    def timeout_handler(signum, frame):
        # Now that flock retries automatically when interrupted, we need
        # an exception to stop it
        # This exception will propagate on the main thread, make sure you're calling flock there
        raise InterruptedError
    original_handler = signal.signal(signal.SIGALRM, timeout_handler)
    try:
        signal.alarm(seconds)
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, original_handler)

def check_lockable_drive(dir):
    lock_file = os.path.join(dir, "test.lck")
    with timeout(3):
        f = open(lock_file, "w")
        try:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            os.remove(lock_file)
            return True
        except InterruptedError:
            # Catch the exception raised by the handler
            # If we weren't raising an exception, flock would automatically retry on signals
            # remove lock file
            os.remove(lock_file)
            return False

def get_free_gpu_memory():
    device_count  = nvmlDeviceGetCount()
    if device_count > 0:
        handle = nvmlDeviceGetHandleByIndex(0)
        mem_info = nvmlDeviceGetMemoryInfo(handle)
        free_memory = mem_info.free/1024/1024/1024
        return free_memory
    else:
        logger.warning("No GPU found, please check your GPU driver.")
        return 0
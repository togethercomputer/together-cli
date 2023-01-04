import os
import subprocess
from loguru import logger
from together_node.src.constants import BINARY_CONFIG
from together_node.src.utility import remote_download, run_command_in_foreground

def check_binary_exists(binary):
    """Check if a binary exists in the path.

    Args:
        binary (str): The binary to check for.

    Returns:
        bool: True if the binary exists, False otherwise.

    """
    try:
        subprocess.check_output(["which", binary])
        return True
    except subprocess.CalledProcessError:
        return False
    
def download_go_together(working_dir: str):
    """Download the go-together binary.

    Args:
        working_dir (str): The working directory to download the binary to.

    Returns:
        str: The path to the downloaded binary.

    """
    # make a "bin" directory in the working directory if it doesn't exist
    bin_dir = os.path.join(working_dir, "bin")
    if not os.path.exists(bin_dir):
        os.makedirs(bin_dir)
    # check if there is any file called "together" in the repository
    # if there is, then we don't need to download it
    if os.path.exists(os.path.join(bin_dir, "together")):
        logger.info("Found go-together binary in the working directory, skipping download it.")
        return os.path.join(bin_dir, "together")
    # download the binary
    logger.info("Downloading go-together binary...")
    remote_download(BINARY_CONFIG["GO-TOGETHER"]["url"], bin_dir)

    run_command_in_foreground(f"chmod +x {os.path.join(bin_dir, 'together')}")
    return os.path.join(bin_dir, "together")
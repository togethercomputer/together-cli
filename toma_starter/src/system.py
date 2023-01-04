import subprocess

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
    

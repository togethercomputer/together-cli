import os
import sys
import json
import shlex
import random
import string
import requests
import subprocess
from loguru import logger
from rich.console import Console
from rich.progress import Progress
from huggingface_hub import list_repo_files

console = Console()

def download_hf_files(hf_name: str, local_path: str):
    all_files = list_repo_files(hf_name)
    urls = [f"https://huggingface.co/{hf_name}/resolve/main/{file_name}" for file_name in all_files]
    if not os.path.exists(local_path):
        os.makedirs(local_path)
    for url in urls:
        remote_download(url, local_path)

def remote_download(remote_url: str, local_path: str):
    print(f"Downloading file from {remote_url} to {local_path} ...")
    filename = remote_url.split('/')[-1]
    local_path = os.path.join(local_path, filename)
    # check if the file already exists
    if os.path.exists(local_path):
        # logger.info(f"File {filename} already exists, skipping download.")
        # logger.info(f"If you want to download the file again, please delete the file at {local_path} first.")
        return

    with Progress(transient=False) as progress:
        with requests.get(remote_url, stream=True) as r:
            with open(local_path, 'wb') as file:
            # Get the total size, in bytes, from the response header
                total_size = int(r.headers.get('Content-Length')) # in bytes
                task = progress.add_task("Downloading", total=total_size)
                # Define the size of the chunk to iterate over (Mb)
                chunk_size = 10 * 1024 * 1024 # in bytes
                # iterate over every chunk and calculate % of total
                for i, chunk in enumerate(r.iter_content(chunk_size=chunk_size)):
                    file.write(chunk)
                    description = f"Downloading <{filename}> {i * chunk_size/1024/1024/1024:.2f}/{total_size/1024/1024/1024:.2f} GB"
                    progress.update(
                        task,
                        completed=i * chunk_size,
                        description=description
                    )

def run_command_in_background(cmd: str):
    args = shlex.split(cmd)
    subprocess.Popen(
        args,
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

def run_command_in_foreground(cmd: str):
    return subprocess.run(cmd, capture_output=True, shell=True)


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    # reads from together home
    default_together_home = os.path.join(os.path.expanduser("~"), "together")
    reusable_id = None
    instances = []
    if not os.path.exists(default_together_home):
        os.makedirs(default_together_home)
    if os.path.exists(os.path.join(default_together_home, "instances.json")):
        with open(os.path.join(default_together_home, "instances.json"), "r") as f:
            instances = json.load(f)

    # find the first stopped instance
    stopped_instance = [instance for instance in instances if instance["status"] == "stopped"]
    if len(stopped_instance) > 0:
        reusable_id = stopped_instance[0]["node_name"]
    if reusable_id is None:
        return ''.join(random.choice(chars) for _ in range(size))
    else:
        return reusable_id


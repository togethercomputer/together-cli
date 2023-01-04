import os
import sys
import shlex
import requests
import subprocess
from rich.progress import Progress

def remote_download(remote_url: str, local_path: str):
    with Progress(transient=True) as progress:
        with requests.get(remote_url, stream=True) as r:
            filename = remote_url.split('/')[-1]
            local_path = os.path.join(local_path, filename)
            with open(local_path, 'wb') as file:
            # Get the total size, in bytes, from the response header
                total_size = int(r.headers.get('Content-Length'))
                task = progress.add_task("Downloading", total=total_size)
                # Define the size of the chunk to iterate over (Mb)
                chunk_size = 10
                # iterate over every chunk and calculate % of total
                for i, chunk in enumerate(r.iter_content(chunk_size=chunk_size)):
                    file.write(chunk)
                    # calculate current percentage
                    # write current % to console, pause for .1ms, then flush console
                    description = f"Downloading {filename} {i * chunk_size/1024/1024/1024:.2f}/{total_size/1024/1024/1024:.2f} GB"
                    progress.update(task, advance=i * chunk_size / total_size * 100, description=description)

def run_command_in_background(cmd: str):
    args = shlex.split(cmd)
    subprocess.Popen(
        args,
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

def run_command_in_foreground(cmd: str):
    return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
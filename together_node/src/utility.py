import os
import sys
import shlex
import requests
import subprocess
from typing import Dict
from loguru import logger
from rich.progress import Progress
from together_node.src.constants import MODEL_CONFIG, SLURM_TEMPLATES_DOCKER

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
    return subprocess.run(cmd, capture_output=True, shell=True)

def makeup_submission_scripts(
        model_name: str,
        is_docker: bool,
        is_singularity: bool,
        additional_args: Dict={},
        working_dir: str=None,
        gpus: str = None,
        queue_name = None,
        account = None,
    ):
    # we should also check if it is running slurm, but skip it for now
    additional_args['worker.model'] = MODEL_CONFIG[model_name]['worker_model']
    # compose sbatch header
    submission_script = SLURM_TEMPLATES_DOCKER
    if is_docker:
        startup_script = MODEL_CONFIG[model_name]["docker_startup_script"]
        # add additional arguments
        for key, value in additional_args.items():
            startup_script = startup_script + f" --{key}={value}"
        submission_script = submission_script.replace("{{DOCKER_STARTUP_SCRIPT}}", startup_script)
        submission_script = submission_script.replace("{{DOCKER_ID}}", MODEL_CONFIG[model_name]["docker_id"])
    submission_script = submission_script.replace("{{TOGETHER_PATH}}", working_dir)
    gpu_num = gpus.split(":")[1]
    CUDA_VISIBLE_DEVICES = ",".join([str(i) for i in range(int(gpu_num))])
    submission_script = submission_script.replace("{{CUDA_VISIBLE_DEVICES}}", CUDA_VISIBLE_DEVICES)
    # now process the headers
    slurm_heads = {
        "job-name": f"together-{model_name}",
        "time":"1:00:00",
        "ntasks":1,
        "cpus-per-task": 4,
        "mem-per-cpu": "8G",
        "output": f"{working_dir}/together-{model_name}-%j.out",
        "error": f"{working_dir}/together-{model_name}-%j.err",
        "partition": queue_name,
        "account": account,
        "gres": f"gpu:{gpus}"
    }
    slurm_head_str = ""
    for key, value in slurm_heads.items():
        slurm_head_str = slurm_head_str + f"#SBATCH --{key}={value} \n"
    submission_script = submission_script.replace("{{SLURM_HEAD}}", slurm_head_str)

    return submission_script
import os
import sys
import shlex
import requests
import subprocess
from typing import Dict
from loguru import logger
from rich.progress import Progress
from together_node.src.templates import generate_slurm_heads
from together_node.src.constants import MODEL_CONFIG, SLURM_TEMPLATES_DOCKER, SLURM_TEMPLATES_SINGULARITY

def remote_download(remote_url: str, local_path: str):
    logger.info(f"Downloading file from {remote_url} to {local_path} ...")
    filename = remote_url.split('/')[-1]
    local_path = os.path.join(local_path, filename)
    # check if the file already exists
    if os.path.exists(local_path):
        logger.info(f"File {filename} already exists, skipping download.")
        logger.info(f"If you want to download the file again, please delete the file at {local_path} first.")
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
                    description = f"Downloading {filename} {i * chunk_size/1024/1024/1024:.2f}/{total_size/1024/1024/1024:.2f} GB"
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

def makeup_docker_startscript(
    model_name: str,
    submission_script:str,
    additional_args: Dict={},
    working_dir: str=None,
    gpus: str = None,
    queue_name = None,
    account = None,
):
    # compose sbatch header
    startup_script = MODEL_CONFIG[model_name]["startup_script"]
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
    return submission_script

def makeup_singularity_startscript(
    model_name: str,
    submission_script:str,
    additional_args: Dict={},
    working_dir: str=None,
    gpus: str = None,
    queue_name:str = None,
    account:str = None,
    together_args: Dict= None,
):
    sif_path_name = os.path.join(
        working_dir,
        "images",
        MODEL_CONFIG[model_name]["sif_name"],
    )
    # check if the sif file exists
    if not os.path.exists(sif_path_name):
        logger.error(f"Cannot find sif file {sif_path_name}")
        raise ValueError(f"Cannot find sif file {sif_path_name}")
    submission_script = submission_script.replace("{{SIF_NAME}}", sif_path_name)
    submission_script = submission_script.replace("{{TOGETHER_PATH}}", working_dir)
    weights_path = os.path.join(
        working_dir,
        "weights",
        model_name,
    )
    submission_script = submission_script.replace("{{WEIGHTS_PATH}}", weights_path)
    return submission_script

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
    additional_args['worker.model'] = MODEL_CONFIG[model_name]['worker_model']
    # we should also check if it is running slurm, but skip it for now
    if is_docker:
        submission_script = makeup_docker_startscript(
            model_name,
            SLURM_TEMPLATES_DOCKER,
            additional_args,
            working_dir,
            gpus,
            queue_name,
            account,
        )
    elif is_singularity:
        submission_script = makeup_singularity_startscript(
            model_name,
            SLURM_TEMPLATES_SINGULARITY,
            additional_args,
            working_dir,
            gpus,
            queue_name,
            account,
        )
    else:
        raise ValueError("Either docker or singularity should be set to True")
    startup_script = MODEL_CONFIG[model_name]["startup_script"]
    # add additional arguments
    for key, value in additional_args.items():
        startup_script = startup_script + f" --{key}={value}"
    submission_script = submission_script.replace("{{STARTUP_SCRIPT}}", startup_script)
    slurm_head_str = generate_slurm_heads(
        model_name,
        working_dir,
        account,
        gpus,
        queue_name,
    )
    submission_script = submission_script.replace("{{SLURM_HEAD}}", slurm_head_str)
    return submission_script
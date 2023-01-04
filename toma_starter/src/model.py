import os
import requests
from rich.progress import Progress
from loguru import logger
from toma_starter.src.system import download_go_together
from toma_starter.src.utility import run_command_in_background, run_command_in_foreground

def download_model_and_weights(
    model_name: str,
    is_docker: bool,
    is_singularity: bool,
    working_dir: str
):
    pass

def serve_model(
        model_name: str,
        queue_name: str,
        working_dir: str
    ):
    # step 1: checking go-together binary and configuration files
    together_bin_path = download_go_together(working_dir)
    logger.info(f"Running go-together binary: {together_bin_path}")
    run_command_in_background(f"ls .")
    # step 2: starting go-together in the background
    run_command_in_background(f"{together_bin_path} start --p2p.addr=any --jsonrpc.http.host=0.0.0.0 --jsonrpc.ws.host=0.0.0.0")
    # step 3: downloading the model singularity/docker container & weights

    # step 3: starting the model singularity/docker container
    
    pass

def compose_start_command():
    pass
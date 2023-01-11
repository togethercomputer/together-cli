import os
from typing import Dict
from loguru import logger
from together_cli.src.clusters.slurm import generate_slurm_script
from together_cli.src.constants import MODEL_CONFIG

def makeup_slurm_scripts(
        model_name: str,
        home_dir: str=None,
        data_dir: str=None,
        gpus: str = None,
        queue_name = None,
        account = None,
        modules = None,
        run_command=None,
        node_list=None,
        duration=None,
    ):
    # generate slurm templates
    slurm_templates = generate_slurm_script(
        model_name=model_name,
        data_dir=data_dir,
        modules=modules,
        account=account,
        gpus=gpus,
        queue_name=queue_name,
        node_list=node_list,
        duration = duration,
    )
    slurm_submission_scripts = slurm_templates.replace("{{COMMAND}}", run_command)
    return slurm_submission_scripts
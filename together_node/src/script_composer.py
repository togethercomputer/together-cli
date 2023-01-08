import os
from typing import Dict
from loguru import logger
from together_node.src.templates import generate_slurm_heads
from together_node.src.constants import MODEL_CONFIG, SLURM_TEMPLATES_DOCKER, SLURM_TEMPLATES_SINGULARITY

def makeup_docker_startscript(
    model_name: str,
    submission_script:str,
    additional_args: Dict={},
    home_dir: str=None,
    data_dir: str=None,
    gpus: str = None,
):
    # compose sbatch header
    startup_script = MODEL_CONFIG[model_name]["startup_script"]
    # add additional arguments
    for key, value in additional_args.items():
        startup_script = startup_script + f" --{key}={value}"
    submission_script = submission_script.replace("{{DOCKER_STARTUP_SCRIPT}}", startup_script)
    submission_script = submission_script.replace("{{DOCKER_ID}}", MODEL_CONFIG[model_name]["docker_id"])
    submission_script = submission_script.replace("{{TOGETHER_HOME_DIR}}", home_dir)
    submission_script = submission_script.replace("{{TOGETHER_DATA_DIR}}", data_dir)
    gpu_num = gpus.split(":")[1]
    CUDA_VISIBLE_DEVICES = ",".join([str(i) for i in range(int(gpu_num))])
    submission_script = submission_script.replace("{{CUDA_VISIBLE_DEVICES}}", CUDA_VISIBLE_DEVICES)
    # now process the headers    
    return submission_script

def makeup_singularity_startscript(
    model_name: str,
    submission_script:str,
    additional_args: Dict={},
    home_dir: str=None,
    data_dir: str=None,
    gpus: str = None,
    queue_name:str = None,
    together_args: Dict= None,
):
    sif_path_name = os.path.join(
        data_dir,
        "images",
        MODEL_CONFIG[model_name]["sif_name"],
    )
    # check if the sif file exists
    if not os.path.exists(sif_path_name):
        logger.error(f"Cannot find sif file {sif_path_name}")
        raise ValueError(f"Cannot find sif file {sif_path_name}")
    submission_script = submission_script.replace("{{SIF_NAME}}", sif_path_name)
    submission_script = submission_script.replace("{{TOGETHER_HOME_DIR}}", home_dir)
    submission_script = submission_script.replace("{{TOGETHER_DATA_DIR}}", data_dir)
    submission_script = submission_script.replace("{{WORKER_MODEL_NAME}}", MODEL_CONFIG[model_name]['worker_model'])
    submission_script = submission_script.replace("{{MODEL_NAME}}", model_name)
    submission_script = submission_script.replace("{{MODEL_TYPE}}", MODEL_CONFIG[model_name]['model_type'])
    return submission_script

def makeup_submission_scripts(
        model_name: str,
        is_docker: bool,
        is_singularity: bool,
        additional_args: Dict={},
        home_dir: str=None,
        data_dir: str=None,
        gpus: str = None,
        queue_name = None,
        account = None,
        modules = None,
    ):
    additional_args['worker.model'] = MODEL_CONFIG[model_name]['worker_model']
    # we should also check if it is running slurm, but skip it for now
    if is_docker:
        submission_script = makeup_docker_startscript(
            model_name,
            SLURM_TEMPLATES_DOCKER,
            additional_args,
            home_dir,
            gpus,
            queue_name,
        )
    elif is_singularity:
        submission_script = makeup_singularity_startscript(
            model_name,
            SLURM_TEMPLATES_SINGULARITY,
            additional_args,
            home_dir=home_dir,
            data_dir=data_dir,
            gpus=gpus,
            queue_name=queue_name,
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
        data_dir,
        account,
        gpus,
        queue_name,
    )
    submission_script = submission_script.replace("{{SLURM_HEAD}}", slurm_head_str)
    # compose load modules
    modules_str = ""
    if modules is not None:
            modules_str += f"module load {modules}"
    submission_script = submission_script.replace("{{MODULES}}", modules_str)
    submission_script = submission_script.replace("{{STARTUP_COMMAND}}", MODEL_CONFIG[model_name]['startup_command'])
    return submission_script
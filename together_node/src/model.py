import os
from loguru import logger
from together_node.src.constants import MODEL_CONFIG
from together_node.src.script_composer import makeup_slurm_scripts
from together_node.src.utility import run_command_in_foreground, remote_download

def download_model_and_weights(
    model_name: str,
    is_docker: bool,
    is_singularity: bool,
    working_dir: str
):
    model_config = MODEL_CONFIG[model_name]
    # images folder
    images_dir = os.path.join(working_dir, "images")
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    # weights folder
    weights_dir = os.path.join(working_dir, "weights", model_name)
    weights_already_exist = os.path.exists(weights_dir)
    
    if is_singularity:
        # download the singularity container
        remote_download(model_config["singularity_url"], images_dir)
        if not weights_already_exist:
            os.makedirs(weights_dir)
            remote_download(model_config["weights_url"], weights_dir)
            # decompress the weights
            logger.info(f"Decompressing the weights to {weights_dir}...")
            run_command_in_foreground(f"tar -xvf {os.path.join(weights_dir, model_config['weights_url'].split('/')[-1])} -C {weights_dir}")
            run_command_in_foreground(f"rm {os.path.join(weights_dir, model_config['weights_url'].split('/')[-1])}")
    # elif is_docker:
    # everything will be automatically downloaded by docker
    # upd: to download weights transparently

def serve_model(
        model_name: str,
        queue_name: str,
        home_dir: str,
        data_dir: str,
        use_docker: bool=False,
        use_singularity: bool=False,
        modules: str="",
        gpus: str="",
        account: str="",
        node_name: str="",
        port: int=5000,
    ):
    # step 0: check if needed to download the model and weights   
    download_model_and_weights(
        model_name,
        is_docker=use_docker, 
        is_singularity=use_singularity,
        working_dir=data_dir
    )
    # step 4: checking submission starting scripts
    submission_script = makeup_slurm_scripts(
        model_name,
        is_docker=use_docker,
        is_singularity=use_singularity,
        home_dir = home_dir,
        data_dir = data_dir,
        gpus = gpus,
        queue_name = queue_name,
        account = account,
        modules = modules,
    )
    logger.info(f"Submission script:{submission_script}")
    # step 4.1: write the submission script to a file
    scripts_dir = os.path.join(data_dir, "scripts")
    if not os.path.exists(scripts_dir):
        os.makedirs(scripts_dir)
    with open(os.path.join(scripts_dir, f"{model_name}.slurm"), "w") as f:
        f.write(submission_script)
    # step 5: starting the submission
    # completed_process = run_command_in_foreground(f"sbatch {os.path.join(scripts_dir, f'{model_name}.slurm')}")
    # logger.info(f"Submission started. {completed_process.stdout}")
    # logger.info(f"stderr: {completed_process.stderr}")

def compose_start_command():
    pass
import os
from loguru import logger
from together_cli.src.constants import MODEL_CONFIG
from together_cli.src.script_composer import makeup_slurm_scripts
from together_cli.src.utility import run_command_in_foreground, remote_download

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
    # weights need to be downloaded anyway
    if not weights_already_exist and "weights_url" in model_config:
        os.makedirs(weights_dir)
        remote_download(model_config["weights_url"], weights_dir)
        # decompress the weights
        logger.info(f"Decompressing the weights to {weights_dir}...")
        run_command_in_foreground(f"tar -xvf {os.path.join(weights_dir, model_config['weights_url'].split('/')[-1])} -C {weights_dir}")
        run_command_in_foreground(f"rm {os.path.join(weights_dir, model_config['weights_url'].split('/')[-1])}")
    
def serve_model(
        model_name: str,
        queue_name: str,
        home_dir: str,
        data_dir: str,
        matchmaker_addr: str,
        tags: str,
        use_docker: bool=False,
        use_singularity: bool=False,
        modules: str="",
        gpus: str="",
        account: str="",
        node_list: str=None,
        port: int=None,
        duration: str="",
    ):
    # step 0: check if needed to download the model and weights   
    download_model_and_weights(
        model_name,
        is_docker=use_docker, 
        is_singularity=use_singularity,
        working_dir=data_dir
    )
    # step 2: generate the actual command to run
    run_command = None
    if use_docker:
        from together_cli.src.backend.docker import generate_docker_script
        run_command = generate_docker_script(
            home_dir=home_dir,
            data_dir=data_dir,
            model_name=model_name,
            tags = tags,
            matchmaker_addr = matchmaker_addr,
            port = port,
        )
    elif use_singularity:
        from together_cli.src.backend.singularity import generate_singularity_script
        run_command = generate_singularity_script(
            home_dir=home_dir,
            data_dir=data_dir,
            model_name=model_name,
            tags = tags,
            matchmaker_addr = matchmaker_addr,
            port = port,
        )
    else:
        raise ValueError("Either docker or singularity should be used.")
    # step 3: checking submission starting scripts
    submission_script = makeup_slurm_scripts(
        model_name,
        home_dir = home_dir,
        data_dir = data_dir,
        gpus = gpus,
        queue_name = queue_name,
        account = account,
        modules = modules,
        run_command=run_command,
        node_list=node_list,
        duration = duration,
    )
    logger.info(f"Submission script:{submission_script}")
    # step 4: write the submission script to a file
    scripts_dir = os.path.join(data_dir, "scripts")
    if not os.path.exists(scripts_dir):
        os.makedirs(scripts_dir)
    with open(os.path.join(scripts_dir, f"{model_name}.slurm"), "w") as f:
        f.write(submission_script)
    # step 5: starting the submission
    completed_process = run_command_in_foreground(f"sbatch {os.path.join(scripts_dir, f'{model_name}.slurm')}")
    print("Submitted to slurm")
    logger.info(f"{completed_process.stdout}")
    logger.info(f"{completed_process.stderr}")

def compose_start_command():
    pass
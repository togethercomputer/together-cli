import os
from loguru import logger
from together_cli.src.clusters import dispatch
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
        cluster:str="",
        dry_run: bool=False,
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
            daemon_mode = True if cluster=='baremetal' else False
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
    if cluster == 'slurm':
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
    elif cluster == 'baremetal':
        submission_script = run_command
    else:
        raise ValueError(f"Unknown cluster type {cluster}")
    if not dry_run:
        dispatch(submission_script=submission_script, model_name=model_name, data_dir=data_dir, cluster_type=cluster)
    else:
        logger.info(f"Submission script is generated as follows:{submission_script}")

def compose_start_command():
    pass
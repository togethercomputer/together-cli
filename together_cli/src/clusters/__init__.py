import os
from loguru import logger
from together_cli.src.utility import run_command_in_foreground, run_command_in_background

def dispatch(
        submission_script:str,
        cluster_type:str,
        model_name: str,
        data_dir: str,
        node_name: str,
    ):
    output = ""
    scripts_dir = os.path.join(data_dir, "scripts")
    if not os.path.exists(scripts_dir):
        os.makedirs(scripts_dir)

    if cluster_type == 'baremetal':
        logger.warning("You are running in baremetal mode - it may take a while to pull the docker image, please wait patiently.")

    if cluster_type=='slurm':
        with open(os.path.join(scripts_dir, f"{model_name}.slurm"), "w") as f:
            f.write(submission_script)
        
        # step 5: starting the submission
        completed_process = run_command_in_foreground(f"sbatch {os.path.join(scripts_dir, f'{model_name}.slurm')}")
        print("Submitted to slurm")
        output = completed_process.stdout

        logger.info(f"{output}")
        logger.info(f"{completed_process.stderr}")

    elif cluster_type == 'baremetal':
        with open(os.path.join(scripts_dir, f"{model_name}.sh"), "w") as f:
            f.write(submission_script)
        # step 5: starting the submission
        completed_process = run_command_in_foreground(f"bash {os.path.join(scripts_dir, f'{model_name}.sh')}")
        output = completed_process.stdout
        logger.info(f"{output}")
        logger.info(f"{completed_process.stderr}")
    
    if cluster_type == 'baremetal':
        logger.info(f"Together-node is now running in the docker container `{output}`")
        logger.info(f"Use `together-cli logs {node_name}` to inspect its logs")
    return output.decode("utf-8")
from typing import Dict

def generate_slurm_heads(
    model_name: str,
    working_dir: str,
    account: str = None,
    gpus: str = None,
    queue_name = None,

):
    slurm_heads = {
        "job-name": f"together-{model_name}",
        "time":"1:00:00",
        "ntasks":1,
        "cpus-per-task": 4,
        "mem-per-cpu": "8G",
        "output": f"{working_dir}/together-{model_name}-%j.out",
        "error": f"{working_dir}/together-{model_name}-%j.err",
        "gpus": f"{gpus}"
    }
    if account:
        slurm_heads["account"] = account
    if queue_name:
        slurm_heads["partition"] = queue_name
    slurm_head_str = ""
    for key, value in slurm_heads.items():
        slurm_head_str = slurm_head_str + f"#SBATCH --{key}={value}\n"
    return slurm_head_str

def generate_singularity_environments(environs: Dict):
    environ_specifiers = ""
    for key, value in environs.items():
        environ_specifiers = environ_specifiers + f"--env {key}={value} \ \n"
    return environ_specifiers
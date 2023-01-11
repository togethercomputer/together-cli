from together_cli.src.core.render import render

SLURM_TEMPLATES = """#!/bin/bash
{{SLURM_HEAD}}

{{MODULES}}

{{COMMAND}}
"""

def generate_slurm_script(
    model_name: str,
    data_dir: str,
    modules: str = None,
    account: str = None,
    gpus: str = None,
    queue_name: str = None,
    node_list: str = None,
    duration: str = None
):
    heads_str = generate_slurm_heads(
        model_name=model_name,
        data_dir=data_dir,
        account=account,
        gpus=gpus,
        queue_name=queue_name,
        node_list=node_list,
        duration = duration,
    )
    return render(
        SLURM_TEMPLATES, 
        slurm_head=heads_str,
        modules = f"module load {modules}" if modules is not None else "",
    )


def generate_slurm_heads(
    model_name: str,
    data_dir: str,
    account: str = None,
    gpus: str = None,
    queue_name = None,
    node_list = None,
    duration=None,
):
    slurm_heads = {
        "job-name": f"together-{model_name}",
        "time":f"{duration}",
        "ntasks":1,
        "cpus-per-task": 4,
        "mem-per-cpu": "8G",
        "output": f"{data_dir}/logs/together-{model_name}-%j.out",
        "error": f"{data_dir}/logs/together-{model_name}-%j.err",
        "gpus": f"{gpus}"
    }
    if account:
        slurm_heads["account"] = account
    if queue_name:
        slurm_heads["partition"] = queue_name
    if node_list:
        slurm_heads["nodelist"] = node_list
    slurm_head_str = ""
    for key, value in slurm_heads.items():
        slurm_head_str = slurm_head_str + f"#SBATCH --{key}={value}\n"
    return slurm_head_str


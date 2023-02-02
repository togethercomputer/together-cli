import os
import json
from rich.table import Table
from datetime import datetime
from together_cli.src.utility import console

def persist_instance(
    node_name: str,
    cluster:str,
    model_name: str,
    home_dir:str,
    data_dir:str,
    queue_name: str,
    tags: str,
    use_docker: bool,
    use_singularity: bool,
    account: str,
    node_list: str,
    gpus: str,
    port: int,
    duration: str,
    job_id: str
):
    default_together_home = os.path.join(os.path.expanduser("~"), "together")
    instances = []
    if not os.path.exists(default_together_home):
        os.makedirs(default_together_home)
    if os.path.exists(os.path.join(default_together_home, "instances.json")):
        with open(os.path.join(default_together_home, "instances.json"), "r") as f:
            instances = json.load(f)
    if use_docker and cluster=='baremetal':
        duration="N/a"
        gpus = os.environ.get("CUDA_VISIBLE_DEVICES", "all")
    instances.append({
        "node_name": node_name,
        "job_id": job_id,
        "cluster": cluster,
        "model_name": model_name,
        "home_dir": home_dir,
        "data_dir": data_dir,
        "queue_name": queue_name,
        "tags": tags,
        "use_docker": use_docker,
        "use_singularity": use_singularity,
        "account": account,
        "node_list": node_list,
        "gpus": gpus,
        "port": port,
        "duration": duration,
        "job_id": job_id,
        "status": "running",
        "started_at": str(datetime.now()),
    })

    with open(os.path.join(default_together_home, "instances.json"), "w+") as f:
        json.dump(instances, f, indent=4)

def pprint_instances():
    default_together_home = os.path.join(os.path.expanduser("~"), "together")
    instances = []
    if not os.path.exists(default_together_home):
        os.makedirs(default_together_home)
    
    if os.path.exists(os.path.join(default_together_home, "instances.json")):
        with open(os.path.join(default_together_home, "instances.json"), "r") as f:
            instances = json.load(f)
    
    table = Table(show_header=True, header_style="bold", title="Instances")
    table.add_column("Node Name", style="dim")
    table.add_column("Job ID", style="dim")
    table.add_column("Cluster", style="dim")
    table.add_column("Model", style="dim")
    table.add_column("Status", style="dim")
    table.add_column("Started at", style="dim")
    table.add_column("Duration", style="dim")
    table.add_column("Queue", style="dim")
    table.add_column("Tags", style="dim")
    table.add_column("GPU", style="dim")
    table.add_column("Port", style="dim")

    for instance in instances:
        table.add_row(
            str(instance["node_name"]),
            str(instance["job_id"]),
            str(instance["cluster"]),
            str(instance["model_name"]),
            str(instance["status"]),
            str(instance["started_at"]),
            str(instance["duration"]) if "duration" in instance else "N/A",
            str(instance["queue_name"]) if "queue_name" in instance else "N/A",
            str(instance["tags"]) if "tags" in instance else "N/A",
            str(instance["gpus"]) if "gpus" in instance else "N/A",
            str(instance["port"]) if "port" in instance else "N/A",
        )
    console.print(table)

def shutdown_instance(job_id: str):
    pass

def fetch_logs(job_id: str):
    default_together_home = os.path.join(os.path.expanduser("~"), "together")
    # read instances.json
    with open(os.path.join(default_together_home, "instances.json"), "r") as f:
        instances = json.load(f)
    # find instance with job_id
    instance = [instance for instance in instances if instance["job_id"] == job_id]
    if len(instance) == 0:
        raise Exception("Instance not found")
    instance = instance[0]
    # now try to fetch logs
    ## case 1: baremetal docker, run docker logs {job_id}
    if instance["use_docker"] and instance["cluster"] == "baremetal":
        os.system(f"docker logs {job_id}")
    ## case 2: slurm - read logs from slurm log file
    elif instance["cluster"] == "slurm":
        pass

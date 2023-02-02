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
    job_id: str,
    virtualization: str,
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
    
    # if node_name does not exist, add it
    if not any([instance["node_name"] == node_name for instance in instances]):
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
            "virtualization": virtualization,
        })
    else:
        # if node_name exists, update it
        for instance in instances:
            if instance["node_name"] == node_name:
                instance["job_id"] = job_id
                instance["cluster"] = cluster
                instance["model_name"] = model_name
                instance["home_dir"] = home_dir
                instance["data_dir"] = data_dir
                instance["queue_name"] = queue_name
                instance["tags"] = tags
                instance["use_docker"] = use_docker
                instance["use_singularity"] = use_singularity
                instance["account"] = account
                instance["node_list"] = node_list
                instance["gpus"] = gpus
                instance["port"] = port
                instance["duration"] = duration
                instance["job_id"] = job_id
                instance["status"] = "running"
                instance["started_at"] = str(datetime.now())
                instance["virtualization"] = virtualization
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
    table.add_column("Virtualization", style="dim")

    for instance in instances:
        if len(str(instance["job_id"]))>14:
            job_id = str(instance["job_id"])[:5]+"..."+str(instance["job_id"])[-5:]
        else:
            job_id = str(instance["job_id"])
        table.add_row(
            str(instance["node_name"]),
            job_id,
            str(instance["cluster"]),
            str(instance["model_name"]),
            str(instance["status"]),
            str(instance["started_at"]),
            str(instance["duration"]) if "duration" in instance else "N/A",
            str(instance["queue_name"]) if "queue_name" in instance else "N/A",
            str(instance["tags"]) if "tags" in instance else "N/A",
            str(instance["gpus"]) if "gpus" in instance else "N/A",
            str(instance["port"]) if "port" in instance else "N/A",
            str(instance["virtualization"]) if "virtualization" in instance else "N/A",
        )
    console.print(table)

def shutdown_instance(node_name: str):
    default_together_home = os.path.join(os.path.expanduser("~"), "together")
    instances = []
    if os.path.exists(os.path.join(default_together_home, "instances.json")):
        with open(os.path.join(default_together_home, "instances.json"), "r") as f:
            instances = json.load(f)
    else:
        raise Exception("No instances found")
    
    instance = [instance for instance in instances if instance["node_name"] == node_name]

    if len(instance) == 0:
        raise Exception("Instance not found")
    instance = instance[0]
    if instance["cluster"] == "baremetal" and instance['virtualization'] == 'docker':
        os.system(f"docker stop {instance['job_id']}")
    # update instance.json
    for instance in instances:
        if instance["node_name"] == node_name:
            instance["status"] = "stopped"
    with open(os.path.join(default_together_home, "instances.json"), "w+") as f:
        json.dump(instances, f, indent=4)

def fetch_logs(node_name: str):
    default_together_home = os.path.join(os.path.expanduser("~"), "together")
    # read instances.json
    with open(os.path.join(default_together_home, "instances.json"), "r") as f:
        instances = json.load(f)
    # find instance with job_id
    instance = [instance for instance in instances if instance["node_name"] == node_name]
    if len(instance) == 0:
        raise Exception("Instance not found")
    instance = instance[0]
    if instance["status"] != "running":
        raise Exception("Instance not running")
    job_id = instance["job_id"]
    # now try to fetch logs
    ## case 1: baremetal docker, run docker logs {job_id}
    if instance["use_docker"] and instance["cluster"] == "baremetal":
        os.system(f"docker logs {job_id}")
    ## case 2: slurm - read logs from slurm log file
    elif instance["cluster"] == "slurm":
        pass

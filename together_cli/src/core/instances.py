import os
import json
from rich.table import Table
from datetime import datetime
from together_cli.src.utility import console

def persist_instance(
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
    
    instances.append({
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
        "status": "pending",
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
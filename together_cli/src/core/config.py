import os
import json
from typing import Dict
home_dir = os.path.expanduser("~")
default_together_home = os.path.join(home_dir, "together")

default_config = {
    "data_dir": os.path.join(default_together_home, "data"),
    "home_dir":os.path.join(default_together_home, "home"),
    "owner_addr":"",
    "last_used_port": 8090
}

def write_config(config: Dict, path: str):
    with open(path, "w+") as f:
        json.dump(config, f)

def read_config(path: str) -> Dict:
    if os.path.exists(path):
        with open(path, "r") as f:
            config = json.load(f)
        return config
    else:
        return default_config
import os
from loguru import logger
from together_cli.src.core.render import render
from together_cli.src.constants import MODEL_CONFIG
from together_cli.src.utility import id_generator

DOCKER_TEMPLATE="""
docker run {{DAEMON_MODE}} --rm --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES --ipc=host \
-e NUM_WORKERS=auto \
-v {{TOGETHER_DATA_DIR}}:/home/user/.together \
-v {{TOGETHER_HOME_DIR}}:/host_together_home \
-v {{TOGETHER_DATA_DIR}}/weights/{{MODEL_NAME}}:/home/user/.together/models/ \
-v {{TOGETHER_HOME_DIR}}/hf:/hf \
-v {{TOGETHER_DATA_DIR}}/scratch:/scratch \
{{CONTAINER_ID}} /usr/local/bin/together-node start --owner {{OWNER}} --name {{NODE_NAME}}  --worker.model {{WORKER_MODEL_NAME}} --datadir /host_together_home --worker.model_dir /home/user/.together/models/ --worker.env "HF_HOME=/hf" --worker.mode local-service --worker.group.alloc each --worker.command {{STARTUP_COMMAND}} {{TAGS}} {{MODEL_TYPE}} {{HTTP_PORT}} {{WS_PORT}} --computer.api {{MATCHMAKER_ADDR}}
"""

def generate_docker_script(
    home_dir:str,
    data_dir:str,
    model_name:str,
    tags:str,
    matchmaker_addr:str,
    port:int,
    daemon_mode:bool,
    owner: str,
):
    node_name = id_generator(size=10)
    worker_model_name = MODEL_CONFIG[model_name]['worker_model']
    model_type=""
    if 'model_type' in MODEL_CONFIG[model_name]:
        model_type = f"--worker.model_type {MODEL_CONFIG[model_name]['model_type']}"
    if tags!="":
        tags = "--worker.tags " + tags
    http_port = f"--jsonrpc.http.port {port}"
    ws_port = f"--jsonrpc.ws.port {port+1}"
    startup_command = MODEL_CONFIG[model_name]['startup_command']
    container_id = MODEL_CONFIG[model_name]['docker_id']
    docker_scripts = render(
        DOCKER_TEMPLATE,
        together_home_dir=home_dir,
        together_data_dir=data_dir,
        model_name=model_name,
        worker_model_name=worker_model_name,
        model_type=model_type,
        startup_command=startup_command,
        container_id=container_id,
        tags = tags,
        matchmaker_addr = matchmaker_addr,
        node_name = node_name,
        http_port = http_port,
        ws_port = ws_port,
        daemon_mode='--detach' if daemon_mode else '',
        owner=owner,
    )
    if daemon_mode:
        # meaning it is running locally, load CUDA_VISIBLE_DEVICES
        if 'CUDA_VISIBLE_DEVICES' not in os.environ:
            logger.warning("You are running together-cli in non-cluster mode, and you don't have CUDA_VISIBLE_DEVICES set, will enable all GPUs by default.")
        cuda_visible_devices = os.environ.get('CUDA_VISIBLE_DEVICES','all')
        docker_scripts = docker_scripts.replace("$CUDA_VISIBLE_DEVICES", cuda_visible_devices)
    return docker_scripts
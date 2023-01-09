from together_node.src.core.render import render

DOCKER_TEMPLATE="""
docker run --rm --gpus '"device=all"' --ipc=host \
-e NUM_WORKERS=auto \
-v {{TOGETHER_DATA_DIR}}:/home/user/.together \
-v {{TOGETHER_HOME_DIR}}:/host_together_home \
-v {{TOGETHER_DATA_DIR}}/weights/{{MODEL_NAME}}:/home/user/.together/models/ \
-v {{TOGETHER_HOME_DIR}}/hf:/hf \
-v {{TOGETHER_DATA_DIR}}/scratch:/scratch \
{{CONTAINER_ID}} /usr/local/bin/together start --worker.model_type {{MODEL_TYPE}} --worker.model {{WORKER_MODEL_NAME}} --datadir /host_together_home --worker.model_dir /home/user/.together/models/ --worker.env "HF_HOME=/hf" --worker.mode local-service --worker.group.alloc each --worker.command {{STARTUP_COMMAND}}
"""

def generate_docker_script(
    home_dir,
    data_dir,
    model_name,
    worker_model_name,
    model_type,
    STARTUP_COMMAND
):
    return render(
        DOCKER_TEMPLATE,
        together_home_dir=home_dir,
        together_data_dir=data_dir,
        MODEL_NAME=model_name,
        WORKER_MODEL_NAME=worker_model_name,
        MODEL_TYPE=model_type,
        STARTUP_COMMAND=STARTUP_COMMAND
    )
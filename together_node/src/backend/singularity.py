from together_node.src.core.render import render

SINGULARITY_TEMPLAE="""
singularity run --nv \
--env NUM_WORKERS=auto \
--env TEMP=/scratch \
--bind {{TOGETHER_HOME_DIR}}:/host_together_home \
--bind {{TOGETHER_DATA_DIR}}/weights/{{MODEL_NAME}}:/home/user/.together/models/ \
--bind {{TOGETHER_HOME_DIR}}/hf:/hf  \
--bind {{TOGETHER_DATA_DIR}}/scratch:/scratch \
{{TOGETHER_DATA_DIR}}/images/{{CONTAINER_ID}} \
/usr/local/bin/together start --worker.model_type {{MODEL_TYPE}} --worker.model {{WORKER_MODEL_NAME}} --datadir /host_together_home --worker.model_dir /home/user/.together/models/ --worker.env "HF_HOME=/hf" --worker.mode local-service --worker.group.alloc each --worker.command {{STARTUP_COMMAND}}
"""


def generate_singularity_script(
    home_dir,
    data_dir,
    model_name,
    worker_model_name,
    model_type,
    startup_command,
    container_id,
):
    return render(
        SINGULARITY_TEMPLAE,
        together_home_dir=home_dir,
        together_data_dir=data_dir,
        model_name=model_name,
        worker_model_name=worker_model_name,
        model_type=model_type,
        startup_command=startup_command,
        container_id=container_id,
    )
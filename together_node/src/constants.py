MODEL_CONFIG = {
    'opt-6.7b': {
        "singularity_url": "https://filedn.eu/lougUsdPvd1uJK2jfOYWogH/toma_models/ft_base_ampere.sif",
        "weights_url":"https://filedn.eu/lougUsdPvd1uJK2jfOYWogH/toma_models/opt-6.7b-tp1.tar.gz",
        "docker_id": "togethercomputer/fastertransformer",
        "startup_script": "/usr/local/bin/together start --config /home/user/cfg.yaml --worker.model_type gpt",
        "sif_name": "ft_base_ampere.sif",
        "worker_model":"opt-6.7b-tp1",
        "model_type": "gpt",
        "startup_command":"/workspace/Port_FasterTransformer/serve.sh"
    },
    'opt-1.3b': {
        "singularity_url": "https://filedn.eu/lougUsdPvd1uJK2jfOYWogH/toma_models/ft_base_ampere.sif",
        "weights_url":"https://filedn.eu/lougUsdPvd1uJK2jfOYWogH/toma_models/opt-1.3b-tp1.tar.gz",
        "worker_model":"opt-1.3b-tp1",
        "docker_id": "togethercomputer/fastertransformer",
        "startup_script": "/usr/local/bin/together start --config /home/user/cfg.yaml --worker.model_type gpt",
        "sif_name": "ft_base_ampere.sif",
        "model_type": "gpt",
        "startup_command":"/workspace/Port_FasterTransformer/serve.sh"
    }
}

BINARY_CONFIG = {
    "GO-TOGETHER": {
        "url":"https://filedn.eu/lougUsdPvd1uJK2jfOYWogH/together",
        "config_url":"",
    },
    "TCM": {
        "url":"https://filedn.eu/lougUsdPvd1uJK2jfOYWogH/tcm",
    }
}

SLURM_TEMPLATES_DOCKER = """#!/bin/bash
{{SLURM_HEAD}}

{{MODULES}}

docker run --rm --gpus '"device={{CUDA_VISIBLE_DEVICES}}"' --ipc=host \
-e NUM_WORKERS=auto \
-v {{TOGETHER_DATA_DIR}}:/home/user/.together \
{{DOCKER_ID}} {{STARTUP_SCRIPT}}
"""

SLURM_TEMPLATES_SINGULARITY = """#!/bin/bash
{{SLURM_HEAD}}
{{MODULES}}
singularity run --nv \
--env NUM_WORKERS=auto \
--env TEMP=/scratch \
--bind {{TOGETHER_HOME_DIR}}:/host_together_home \
--bind {{TOGETHER_DATA_DIR}}/weights/{{MODEL_NAME}}:/home/user/.together/models/ \
--bind {{TOGETHER_HOME_DIR}}/hf:/hf  \
--bind {{TOGETHER_DATA_DIR}}/scratch:/scratch \
{{TOGETHER_DATA_DIR}}/images/ft_base_ampere.sif \
/usr/local/bin/together start --worker.model_type {{MODEL_TYPE}} --worker.model {{WORKER_MODEL_NAME}} --datadir /host_together_home --worker.model_dir /home/user/.together/models/ --worker.env "HF_HOME=/hf" --worker.mode local-service --worker.group.alloc each --worker.command {{STARTUP_COMMAND}}
"""
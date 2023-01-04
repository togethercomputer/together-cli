MODEL_CONFIG = {
    'OPT-6.7B': {
        "singularity_url": "https://filedn.eu/lougUsdPvd1uJK2jfOYWogH/toma_models/ft_base_ampere.sif",
        "weights_url":"https://filedn.eu/lougUsdPvd1uJK2jfOYWogH/toma_models/opt-6.7b-tp1.tar.gz",
        "worker_model":"opt-6.7b-tp1",
        "docker_id": "togethercomputer/fastertransformer",
        "docker_startup_script": "/usr/local/bin/together start --config /home/user/cfg.yaml --worker.model_type gpt"
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

docker run --rm --gpus '"device={{CUDA_VISIBLE_DEVICES}}"' --ipc=host \
-e NUM_WORKERS=auto \
-v {{TOGETHER_PATH}}:/home/user/.together \
{{DOCKER_ID}} {{DOCKER_STARTUP_SCRIPT}}
"""
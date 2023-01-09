MODEL_CONFIG = {
    'opt-6.7b': {
        "singularity_url": "https://filedn.eu/lougUsdPvd1uJK2jfOYWogH/toma_models/ft_base_ampere.sif",
        "weights_url":"https://filedn.eu/lougUsdPvd1uJK2jfOYWogH/toma_models/opt-6.7b-tp1.tar.gz",
        "docker_id": "togethercomputer/fastertransformer",
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
        "sif_name": "ft_base_ampere.sif",
        "model_type": "gpt",
        "startup_command":"/workspace/Port_FasterTransformer/serve.sh"
    },
    'StableDiffusion': {
        "singularity_url": "https://filedn.eu/lougUsdPvd1uJK2jfOYWogH/toma_models/ft_base_ampere.sif",
        "weights_url":"https://filedn.eu/lougUsdPvd1uJK2jfOYWogH/toma_models/opt-1.3b-tp1.tar.gz",
        "worker_model":"opt-1.3b-tp1",
        "docker_id": "togethercomputer/fastertransformer",
        "sif_name": "ft_base_ampere.sif",
        "model_type": "gpt",
        "startup_command":"/workspace/Port_FasterTransformer/serve.sh"
    }
}

BINARY_CONFIG = {
    "GO-TOGETHER": {
        "url":"https://filedn.eu/lougUsdPvd1uJK2jfOYWogH/together",
        "config_url":"",
    }
}
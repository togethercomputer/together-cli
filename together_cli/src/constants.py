MODEL_CONFIG = {
    'opt-6.7b': {
        "singularity_url": "https://filedn.eu/lougUsdPvd1uJK2jfOYWogH/toma_models/ft_base_ampere.sif",
        "weights_url":"https://filedn.eu/lougUsdPvd1uJK2jfOYWogH/toma_models/opt-6.7b-tp1.tar.gz",
        "docker_image": "xzyaoi/faster_transformer:ampere",
        "sif_name": "ft_base_ampere.sif",
        "worker_model":"opt-6.7b-tp1",
        "model_type": "gpt",
        "startup_command":"/workspace/Port_FasterTransformer/serve.sh"
    },
    'opt-1.3b': {
        "singularity_url": "https://filedn.eu/lougUsdPvd1uJK2jfOYWogH/toma_models/ft_base_ampere.sif",
        "weights_url":"https://filedn.eu/lougUsdPvd1uJK2jfOYWogH/toma_models/opt-1.3b-tp1.tar.gz",
        "worker_model":"opt-1.3b-tp1",
        "docker_image": "xzyaoi/faster_transformer:ampere",
        "sif_name": "ft_base_ampere.sif",
        "model_type": "gpt",
        "startup_command":"/workspace/Port_FasterTransformer/serve.sh"
    },
    'stable-diffusion': {
        "singularity_url": "https://filedn.eu/lougUsdPvd1uJK2jfOYWogH/toma_models/stablediffusion_general.sif",
        "worker_model":"StableDiffusion",
        "docker_image": "xzyaoi/stablediffusion:general",
        "sif_name": "stablediffusion_general.sif",
        "startup_command":"/home/user/serve.sh"
    },
    'gpt-jt': {
        "singularity_url": "https://together-singularity.s3.us-west-2.amazonaws.com/ft_base_ampere.sif",
        "weights_url":"https://together-singularity.s3.us-west-2.amazonaws.com/gpt-jt-6b-v1.tar.gz",
        "worker_model":"GPT-JT-6B-v1-tp1",
        "docker_image": "xzyaoi/faster_transformer:ampere",
        "sif_name": "ft_base_ampere.sif",
        "model_type": "gptj",
        "startup_command":"/workspace/Port_FasterTransformer/serve.sh"
    },
    'gpt-neoxt-v0.6':{
        "singularity_url": "https://together-singularity.s3.us-west-2.amazonaws.com/native_hf_model.sif",
        "weights_url":"https://together-singularity.s3.us-west-2.amazonaws.com/GPT-NeoXT-20B-chat-v0.6.tar.gz",
        "worker_model":"together/gpt-neoxT-20B-chat-latest",
        "docker_image": "xzyaoi/faster_transformer:ampere",
        "sif_name": "native_hf_model.sif",
        "model_type": "",
        "startup_command":"/app/serve_neoxt.sh"
    }
}

BINARY_CONFIG = {
    "GO-TOGETHER": {
        "url":"https://filedn.eu/lougUsdPvd1uJK2jfOYWogH/together",
        "config_url":"",
    }
}
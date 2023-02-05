MODEL_CONFIG = {
    'h3-125m':{
        "singularity_url": "https://together-singularity.s3.us-west-2.amazonaws.com/h3-0.0.1.sif",
        "weights_url":"https://together-singularity.s3.us-west-2.amazonaws.com/H3-125M.tar.gz",
        "worker_model":"together/h3-125m",
        "docker_image": "xzyaoi/h3:0.0.1",
        "sif_name": "h3-0.0.1.sif",
        "model_type": "",
        "startup_command":"/workspace/H3/serve_125m.sh",
        "together_name":"together/h3-125m"
    },
    'h3-2.7b':{
        "singularity_url": "https://together-singularity.s3.us-west-2.amazonaws.com/h3-0.0.1.sif",
        "weights_url":"https://together-singularity.s3.us-west-2.amazonaws.com/H3-2.7B.tar.gz",
        "worker_model":"together/h3-2.7b",
        "docker_image": "xzyaoi/h3:0.0.1",
        "sif_name": "h3-0.0.1.sif",
        "model_type": "",
        "startup_command":"/workspace/H3/serve_2.7b.sh",
        "together_name":"together/h3-2.7b"
    },
    'h3-1.3b':{
        "singularity_url": "https://together-singularity.s3.us-west-2.amazonaws.com/h3-0.0.1.sif",
        "weights_url":"https://together-singularity.s3.us-west-2.amazonaws.com/H3-1.3B.tar.gz",
        "worker_model":"together/h3-1.3b",
        "docker_image": "xzyaoi/h3:0.0.1",
        "sif_name": "h3-0.0.1.sif",
        "model_type": "",
        "startup_command":"/workspace/H3/serve_1.3b.sh",
        "together_name":"together/h3-1.3b"
    },
    'h3-355m':{
        "singularity_url": "https://together-singularity.s3.us-west-2.amazonaws.com/h3-0.0.1.sif",
        "weights_url":"https://together-singularity.s3.us-west-2.amazonaws.com/H3-355M.tar.gz",
        "worker_model":"together/h3-355m",
        "docker_image": "xzyaoi/h3:0.0.1",
        "sif_name": "h3-0.0.1.sif",
        "model_type": "",
        "startup_command":"/workspace/H3/serve_355m.sh",
        "together_name":"together/h3-355m"
    },
    'opt-1.3b': {
        "singularity_url": "https://filedn.eu/lougUsdPvd1uJK2jfOYWogH/toma_models/ft_base_ampere.sif",
        "weights_url":"https://filedn.eu/lougUsdPvd1uJK2jfOYWogH/toma_models/opt-1.3b-tp1.tar.gz",
        "worker_model":"opt-1.3b-tp1",
        "docker_image": "xzyaoi/faster_transformer:0.0.1",
        "sif_name": "ft_base_ampere.sif",
        "model_type": "gpt",
        "startup_command":"/workspace/Port_FasterTransformer/serve.sh",
        "together_name":"opt-1.3b-tp1"
    },
    'opt-6.7b': {
        "singularity_url": "https://filedn.eu/lougUsdPvd1uJK2jfOYWogH/toma_models/ft_base_ampere.sif",
        "weights_url":"https://filedn.eu/lougUsdPvd1uJK2jfOYWogH/toma_models/opt-6.7b-tp1.tar.gz",
        "docker_image": "xzyaoi/faster_transformer:0.0.1",
        "sif_name": "ft_base_ampere.sif",
        "worker_model":"opt-6.7b-tp1",
        "model_type": "gpt",
        "startup_command":"/workspace/Port_FasterTransformer/serve.sh",
        "together_name":"opt-6.7b-tp1",
    },
    'gpt-jt': {
        "singularity_url": "https://together-singularity.s3.us-west-2.amazonaws.com/ft_base_ampere.sif",
        "weights_url":"https://together-singularity.s3.us-west-2.amazonaws.com/gpt-jt-6b-v1.tar.gz",
        "worker_model":"GPT-JT-6B-v1-tp1",
        "docker_image": "xzyaoi/faster_transformer:0.0.1",
        "sif_name": "ft_base_ampere.sif",
        "model_type": "gptj",
        "startup_command":"/workspace/Port_FasterTransformer/serve.sh",
        "together_name":"together/gpt-jt-6b-v1"
    },
    'gpt-neoxt-v0.6':{
        "singularity_url": "https://together-singularity.s3.us-west-2.amazonaws.com/native_hf_model.sif",
        "weights_url":"https://together-singularity.s3.us-west-2.amazonaws.com/GPT-NeoXT-20B-chat-v0.6.tar.gz",
        "worker_model":"together/gpt-neoxT-20B-chat-latest",
        "docker_image": "xzyaoi/native_hf_models:0.0.1",
        "sif_name": "native_hf_model.sif",
        "model_type": "",
        "startup_command":"/app/serve_neoxt.sh",
        "together_name":"together/gpt-neoxT-20B-chat-latest"
    },
    'stable-diffusion': {
        "singularity_url": "https://filedn.eu/lougUsdPvd1uJK2jfOYWogH/toma_models/stablediffusion_general.sif",
        "worker_model":"StableDiffusion",
        "docker_image": "xzyaoi/stablediffusion:general",
        "sif_name": "stablediffusion_general.sif",
        "startup_command":"/home/user/serve.sh",
        "together_name":"StableDiffusion"
    },
}

BINARY_CONFIG = {
    "GO-TOGETHER": {
        "url":"https://filedn.eu/lougUsdPvd1uJK2jfOYWogH/together",
        "config_url":"",
    }
}
MODEL_CONFIG = {
    'h3-125m-h3':{
        "singularity_url": "https://together-singularity.s3.us-west-2.amazonaws.com/h3-0.0.1.sif",
        "weights_url":"https://together-singularity.s3.us-west-2.amazonaws.com/H3-125M.tar.gz",
        "worker_model":"together/h3-125m",
        "docker_image": "xzyaoi/h3:0.0.3",
        "sif_name": "h3-0.0.1.sif",
        "startup_command":"/workspace/H3/serve_125m.sh",
        "together_name":"h3-125m-h3",
        "min_gpu_memory": 2
    },
    'h3-2.7b-h3':{
        "singularity_url": "https://together-singularity.s3.us-west-2.amazonaws.com/h3-0.0.1.sif",
        "weights_url":"https://together-singularity.s3.us-west-2.amazonaws.com/H3-2.7B.tar.gz",
        "worker_model":"together/h3-2.7b",
        "docker_image": "xzyaoi/h3:0.0.3",
        "sif_name": "h3-0.0.1.sif",
        "startup_command":"/workspace/H3/serve_2.7b.sh",
        "together_name":"h3-2.7b-h3",
        "min_gpu_memory": 16
    },
    'h3-1.3b-h3':{
        "singularity_url": "https://together-singularity.s3.us-west-2.amazonaws.com/h3-0.0.1.sif",
        "weights_url":"https://together-singularity.s3.us-west-2.amazonaws.com/H3-1.3B.tar.gz",
        "worker_model":"together/h3-1.3b",
        "docker_image": "xzyaoi/h3:0.0.3",
        "sif_name": "h3-0.0.1.sif",
        "startup_command":"/workspace/H3/serve_1.3b.sh",
        "together_name":"h3-1.3b-h3",
        "min_gpu_memory": 8
    },
    'h3-355m-h3':{
        "singularity_url": "https://together-singularity.s3.us-west-2.amazonaws.com/h3-0.0.1.sif",
        "weights_url":"https://together-singularity.s3.us-west-2.amazonaws.com/H3-355M.tar.gz",
        "worker_model":"together/h3-355m",
        "docker_image": "xzyaoi/h3:0.0.3",
        "sif_name": "h3-0.0.1.sif",
        "startup_command":"/workspace/H3/serve_355m.sh",
        "together_name":"h3-355m-h3",
        "min_gpu_memory": 16
    },
    'opt-1.3b-ft-tp1': {
        "singularity_url": "https://filedn.eu/lougUsdPvd1uJK2jfOYWogH/toma_models/ft_base_ampere.sif",
        "weights_url":"https://together-singularity.s3.us-west-2.amazonaws.com/opt-1.3b-tp1.tar.gz",
        "worker_model":"opt-1.3b-tp1",
        "docker_image": "xzyaoi/faster_transformer:0.0.3",
        "sif_name": "ft_base_ampere.sif",
        "model_type": "gpt",
        "startup_command":"/workspace/Port_FasterTransformer/serve.sh",
        "together_name":"opt-1.3b-ft-tp1",
        "min_gpu_memory": 3
    },
    'opt-6.7b-ft-tp1': {
        "singularity_url": "https://filedn.eu/lougUsdPvd1uJK2jfOYWogH/toma_models/ft_base_ampere.sif",
        "weights_url":"https://together-singularity.s3.us-west-2.amazonaws.com/opt-6.7b-tp1.tar.gz",
        "docker_image": "xzyaoi/faster_transformer:0.0.3",
        "sif_name": "ft_base_ampere.sif",
        "worker_model":"opt-6.7b-tp1",
        "model_type": "gpt",
        "startup_command":"/workspace/Port_FasterTransformer/serve.sh",
        "together_name":"opt-6.7b-ft-tp1",
        "min_gpu_memory": 16
    },
    'gpt-jt-6b-v1-ft-tp1': {
        "singularity_url": "https://together-singularity.s3.us-west-2.amazonaws.com/ft_base_ampere.sif",
        "weights_url":"https://together-singularity.s3.us-west-2.amazonaws.com/gpt-jt-6b-v1.tar.gz",
        "worker_model":"GPT-JT-6B-v1-tp1",
        "docker_image": "xzyaoi/faster_transformer:0.0.3",
        "sif_name": "ft_base_ampere.sif",
        "model_type": "gptj",
        "startup_command":"/workspace/Port_FasterTransformer/serve.sh",
        "together_name":"gpt-jt-6b-v1-ft-tp1",
        "min_gpu_memory": 16
    },
    'universal-sd':{
        "singularity_url": "https://together-singularity.s3.us-west-2.amazonaws.com/h3-0.0.1.sif",
        "worker_model":"UniversalStableDiffusion",
        "docker_image": "xzyaoi/universal-sd:0.0.3",
        "sif_name": "usd-0.0.1.sif",
        "startup_command":"/app/serve.sh",
        "together_name":"universal-sd",
        "min_gpu_memory": 8
    },
    "flan-t5-xxl-hf":{
        "singularity_url": "https://together-singularity.s3.us-west-2.amazonaws.com/native_hf_model.sif",
        "worker_model":"flan-t5-xxl",
        "docker_image": "xzyaoi/native_hf_models:0.0.3",
        "sif_name": "flan-t5-xxl.sif",
        "from_hf":"google/flan-t5-xxl",
        "startup_command": "/app/serve_flant5xxl.sh",
        "together_name":"flan-t5-xxl-hf",
        "min_gpu_memory": 32
    },
    "opt-iml-30b-hf":{
        "singularity_url": "https://together-singularity.s3.us-west-2.amazonaws.com/native_hf_model.sif",
        "worker_model":"opt-iml-30b",
        "docker_image": "xzyaoi/native_hf_models:0.0.3",
        "sif_name": "native_hf_model.sif",
        "from_hf":"facebook/opt-iml-30b",
        "startup_command": "/app/serve_opt_iml_30b.sh",
        "together_name":"opt-iml-30b-hf",
        "min_gpu_memory": 60
    },
    "codegen-mono-16b-hf":{
        "singularity_url": "https://together-singularity.s3.us-west-2.amazonaws.com/native_hf_model.sif",
        "worker_model":"codegen-16b-mono",
        "docker_image": "xzyaoi/native_hf_models:0.0.3",
        "sif_name": "native_hf_model.sif",
        "from_hf":"Salesforce/codegen-16b-mono",
        "startup_command": "/app/serve_codegen_16b_mono.sh",
        "together_name":"codegen-mono-16b-hf",
        "min_gpu_memory": 32
    },
    # "chip-20b":{
    #     "singularity_url": "https://together-singularity.s3.us-west-2.amazonaws.com/native_hf_model.sif",
    #     "worker_model":"chip-20b",
    #     "docker_image": "xzyaoi/native_hf_models:0.0.2",
    #     "sif_name": "native_hf_model.sif",
    #     "from_hf":"Rallio67/chip_20B_instruct_alpha",
    #     "startup_command": "/app/serve_chip_20b.sh",
    #     "together_name":"together/chip_20b_instruct_alpha"
    # },
    # "glm-130b":{
    #     "singularity_url": "https://together-singularity.s3.us-west-2.amazonaws.com/glm.sif",
    #     "weights_url":"https://together-singularity.s3.us-west-2.amazonaws.com/glm-130b.tar.gz",
    #     "worker_model":"glm-130b",
    #     "docker_image": "xzyaoi/glm:0.0.1",
    #     "sif_name": "glm.sif",
    #     "startup_command": "/app/start_dist_glm.sh",
    #     "together_name":"together/glm-130b"
    # },
}

BINARY_CONFIG = {
    "GO-TOGETHER": {
        "url":"https://filedn.eu/lougUsdPvd1uJK2jfOYWogH/together",
        "config_url":"",
    }
}
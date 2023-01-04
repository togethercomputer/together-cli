#!/bin/bash

{{SLURM_HEAD}}

docker run --rm --gpus '"device={{CUDA_VISIBLE_DEVICES}}"' --ipc=host \
-e NUM_WORKERS=auto \
-v {{TOGETHER_PATH}}:/home/user/.together \
{{DOCKER_ID}} /usr/local/bin/together start \
--color --config /home/user/cfg.yaml --worker.model {{MODEL_NAME}} --worker.model_type gpt

#SBATCH --partition={{PARTITION}}

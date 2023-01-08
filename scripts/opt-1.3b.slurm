#!/bin/bash
#SBATCH --job-name=together-opt-1.3b
#SBATCH --time=1:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=8G
#SBATCH --output=.cache/logs/together-opt-1.3b-%j.out
#SBATCH --error=.cache/logs/together-opt-1.3b-%j.err
#SBATCH --gpus=titanrtx:1

module load eth_proxy python_gpu/3.9.9
singularity run --nv --env NUM_WORKERS=auto --env TEMP=/scratch --bind ./together:/host_together_home --bind .cache/weights/:/home/user/.together/models/ --bind ./hf:/hf  --bind .cache/scratch:/scratch .cache/images/ft_base_ampere.sif /usr/local/bin/together start --worker.model_type gpt --worker.model opt-1.3b-tp1 --datadir /host_together_home --worker.model_dir /home/user/.together/models/ --worker.env "HF_HOME=/hf"

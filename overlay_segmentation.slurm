#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --time=0:20:00
#SBATCH --mem=128Gb
#SBATCH --cpus-per-task=8
#SBATCH -A christlab
#SBATCH --output=/dev/null

#SBATCH --partition=standard

LOG_DIR="${2}/log"
mkdir -p $LOG_DIR

TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)

output_log="$LOG_DIR/output_${SLURM_JOB_ID}_$TIMESTAMP.log"
error_log="$LOG_DIR/error_${SLURM_JOB_ID}_$TIMESTAMP.log"

exec 1>${output_log}
exec 2>${error_log}

PY_SCRIPT="/scratch/$(whoami)/rivanna_cellpose/overlay_segmentation.py"

echo Processing "${1}"

python3 $PY_SCRIPT "${1}"

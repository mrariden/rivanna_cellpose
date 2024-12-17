#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --time=1:30:00
#SBATCH --mem=128Gb
#SBATCH --cpus-per-task=8
#SBATCH -A christlab
#SBATCH --output=/dev/null

#SBATCH --gres=gpu:a100:1
#SBATCH --partition=gpu


LOG_DIR="${2}/log"
mkdir -p $LOG_DIR

TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)

output_log="$LOG_DIR/output_${SLURM_JOB_ID}_$TIMESTAMP.log"
error_log="$LOG_DIR/error_${SLURM_JOB_ID}_$TIMESTAMP.log"

exec 1>${output_log}
exec 2>${error_log}

module load apptainer
module load cellpose

# maybe some stuff that could go into env vars?
PY_CMD="apptainer exec ${CONTAINERDIR}/cellpose-3.0.10.sif python"
RVCP_CMD="apptainer run --nv ${CONTAINERDIR}/cellpose-3.0.10.sif -m cellpose"
RVCP_DIR="/scratch/$(whoami)/rivanna_cellpose"

echo Processing "${1}"

res=$($PY_CMD $RVCP_DIR/get_image_file_resolution.py "${1}")
echo Resolution: $res

diam=$(echo "60 * $res * 1.75" | bc)
echo Using diameter: $diam
echo Saving to dir: "${2}"

$RVCP_CMD --use_gpu\
     --image_path "${1}"\
     --chan 1\
     --chan2 3\
	 --diameter $diam\
	 --save_png\
	 --no_npy\
     --verbose\
	 --savedir "${2}"\
	 --pretrained_model $RVCP_DIR/CP_20240822_124148-laminin-actin 


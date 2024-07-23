#!/bin/bash
#SBATCH --partition=defq
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=40g
#SBATCH --time=7-00:00:00
#SBATCH --array=0-99


module load java-uon/jdk-11.0.1
echo "Running on `hostname`"
cd ${SLURM_SUBMIT_DIR}

for i in {0..489}; do
    if [[ $((i%100)) == ${SLURM_ARRAY_TASK_ID} ]]; then
        python3 extract_midpoint_rooted.py $i
    fi
done

sleep 40
echo "Finished job now"

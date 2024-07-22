#!/bin/bash
#SBATCH --partition=defq
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --mem=8g
#SBATCH --time=7-00:00:00

echo "Running on `hostname`"
conda activate busco
cd ${SLURM_SUBMIT_DIR}

while read l; do
    sp=$(awk -F, '{print $1}' <<< "$l")
    path=$(awk -F, '{print $3}' <<< "$l")
    busco -i total_proteomes/$path -m prot -o busco_results/${sp} -l eukaryota -c 16 -f
done < directory_to_accession.csv

sleep 40

echo "Finished job now"

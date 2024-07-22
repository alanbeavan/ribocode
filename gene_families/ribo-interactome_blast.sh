#!/bin/bash
#SBATCH --job-name=ribo_blast
#SBATCH --partition=defq
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --mem=8g
#SBATCH --time=7-00:00:00

echo "Running on `hostname`"
cd ${SLURM_SUBMIT_DIR}

module load blast-uoneasy/2.10.1-gompi-2020a
array=(ribo-interactome_families/*)
NLINES=$(ls ribo-interactome_families/ | wc -l)


for ((i=0; i<$NLINES; i++)); do
    echo $i
    out=$(basename ${array[$i]})
    blastp -outfmt 6 -db singledb/db -query ${array[$i]} -out ribo-interactome_blast_results/${out}.csv -evalue 10e-3 -max_target_seqs 10000 -num_threads 16
done


sleep 40

echo "Finished job now"

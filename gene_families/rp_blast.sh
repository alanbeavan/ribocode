#!/bin/bash
#SBATCH --job-name=rp_blast
#SBATCH --partition=defq
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --mem=8g
#SBATCH --time=1-00:00:00
#SBATCH --array=0-79

echo "Running on `hostname`"
cd ${SLURM_SUBMIT_DIR}

module load blast-uoneasy/2.10.1-gompi-2020a
array=(families/RP_fams/*)
NLINES=$(ls families/RP_fams/ | wc -l)
echo $NLINES

for ((i=0; i<$NLINES; i++)); do
    if (( $i  == ${SLURM_ARRAY_TASK_ID} )); then
        echo $i
        out=$(basename ${array[$i]})
        blastp -outfmt 6 -db singledb/db -query ${array[$i]}/all_protein.fa -out rp_blast_results/${out}.csv -evalue 10e-3 -max_target_seqs 10000 -num_threads 16
    fi
done


sleep 40

echo "Finished job now"

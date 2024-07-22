#!/bin/bash
#SBATCH --job-name=fly_blast
#SBATCH --partition=defq
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=8g
#SBATCH --time=7-00:00:00

echo "Running on `hostname`"
cd ${SLURM_SUBMIT_DIR}

module load blast-uoneasy/2.10.1-gompi-2020a
array=(fly_RAPs/families/*)
NLINES=$(ls fly_RAPs/families/* | wc -l)
echo $NLINES

for ((i=0; i<$NLINES; i++)); do
    out=$(basename ${array[$i]})
    blastp -outfmt 6 -db singledb/db -query ${array[$i]} -out fly_RAP_blast_results/${out}.csv -evalue 10e-3 -max_target_seqs 10000 -num_threads 16
done

array=(fly_biogenesis_factors/families/*)
NLINES=$(ls fly_biogenesis_factors/families/* | wc -l)
echo $NLINES
for ((i=0; i<$NLINES; i++)); do
    out=$(basename ${array[$i]})
    blastp -outfmt 6 -db singledb/db -query ${array[$i]} -out fly_biogenesis_factors_blast_results/${out}.csv -evalue 10e-3 -max_target_seqs 10000 -num_threads 16
done


sleep 40

echo "Finished job now"

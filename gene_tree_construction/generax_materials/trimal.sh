#!/bin/bash
#SBATCH --partition=defq
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=20g
#SBATCH --time=7-00:00:0

echo "Running on `hostname`"
cd ${SLURM_SUBMIT_DIR}

for file in alignments/*/aln.aln.fa.longest_peptides_from_headers.smaller;
do
    #trimal -in $file -out ${file}.trimmed.gappyout -gappyout
    trimal -in $file -out ${file}.trimmed.gt50 -gt 0.5
    #trimal -in $file -out ${file}.trimmed.gt50st50 -gt 0.5 -st 0.5
done
    

sleep 40
echo "Finished job now"

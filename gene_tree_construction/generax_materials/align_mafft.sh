#!/bin/bash
#SBATCH --partition=defq
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=40g
#SBATCH --time=3:00:00
#SBATCH --array 0-568
#change for 0 if rerun

module load java-uon/jdk-11.0.1
echo "Running on `hostname`"
cd ${SLURM_SUBMIT_DIR}
i=0

for file in alignments/*;
do
    if [ $i == ${SLURM_ARRAY_TASK_ID} ];
    then
      mafft --anysymbol ${file}/aln.fa.longest_peptides_from_headers.fa.smaller > ${file}/aln.aln.fa.longest_peptides_from_headers.smaller
    fi
    i=$((i+1))
done

sleep 40
echo "Finished job now"

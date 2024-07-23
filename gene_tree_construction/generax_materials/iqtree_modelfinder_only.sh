#!/bin/bash
#SBATCH --partition=defq
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=16g
#SBATCH --time=7-00:00:00
#SBATCH --array 0-568


module load java-uon/jdk-11.0.1
echo "Running on `hostname`"
cd ${SLURM_SUBMIT_DIR}
i=0

for file in alignments/*;
do
    if [ $i == ${SLURM_ARRAY_TASK_ID} ];
    then
      mafft --anysymbol ${file}/aln.fa.longest_peptides_from_headers.fa.smaller > ${file}/aln.aln.fa.longest_peptides_from_headers.smaller
      trimal -in ${file}/aln.aln.fa.longest_peptides_from_headers.smaller -out ${file}/aln.aln.fa.longest_peptides_from_headers.smaller.trimmed.gt50 -gt 0.5
      python3 remove_sequences.py 80 ${file}/aln.aln.fa.longest_peptides_from_headers.smaller.trimmed.gt50 ${file}/aln.aln.fa.longest_peptides_from_headers.smaller.trimmed.gt50.filtered
      iqtree -redo -m MF --mset raxml -s ${file}/aln.aln.fa.longest_peptides_from_headers.smaller.trimmed.gt50.filtered
    fi
    i=$((i+1))
done

sleep 40
echo "Finished job now"

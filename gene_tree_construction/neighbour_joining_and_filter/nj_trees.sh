#!/bin/bash
#SBATCH --partition=defq
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=20g
#SBATCH --time=7-00:00:00

echo "Running on `hostname`"
cd ${SLURM_SUBMIT_DIR}

for i in {0..489}; do
    if [ ! -f alignments/group_${i}.aln.mafft ]; then
        mafft merged_by_50/group_${i}.fa > alignments/group_${i}.aln.mafft
    fi
    fasttree alignments/group_${i}.aln.mafft > nj_trees/group_${i}_nj.tree
done

sleep 40

echo "Finished job now"

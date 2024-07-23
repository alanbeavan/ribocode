#!/bin/bash
#SBATCH --partition=defq
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=40g
#SBATCH --time=7-00:00:00
#SBATCH --array=0-69

echo "Running on `hostname`"
cd ${SLURM_SUBMIT_DIR}

j=0
for i in 24 325 19 267 36 92 264 180 108 294 361 124 103 60 373 8 256 41 237 248 280 281 287 295 301 314 316 318 342 398 402 412 427 454 467 486 146 85 28 53 120 55 132 63 80 88 102 83 395 33 44 20 42 6 9 22 34 10 29 30 15 17 16 4 2 3 5 7 12 1; do
    if [[ $j == ${SLURM_ARRAY_TASK_ID} ]]; then
        echo $i
        if [ ! -f alignments/group_${i}.aln.mafft ]; then
            mafft merged_by_50/group_${i}.fa > alignments/group_${i}.aln.mafft
        fi
        fasttree alignments/group_${i}.aln.mafft > nj_trees/group_${i}_nj.tree
    fi
    j=$((j+1))
done

sleep 40
echo "Finished job now"

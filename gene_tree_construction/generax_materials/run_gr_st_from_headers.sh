#!/bin/bash
#SBATCH --partition=defq
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=96
#SBATCH --mem=360g
#SBATCH --time=7-00:00:00

module load java-uon/jdk-11.0.1
echo "Running on `hostname`"
cd ${SLURM_SUBMIT_DIR}

mpiexec -np 96 ~/GeneRax/build/bin/generax -r UndatedDL -f generax_RP_only_starting_trees_lcp_from_headers.families -s tree_no_hordeum.nwk -p RP_only_DL_starting_trees_from_headers

sleep 40
echo "Finished job now"

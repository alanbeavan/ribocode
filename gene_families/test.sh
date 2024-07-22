array=(families/RP_fams/*)
NLINES=$(ls families/RP_fams/ | wc -l)
echo $NLINES


for ((i=0; i<$NLINES; i++)); do
    if (( $i  == 1 )); then
        echo $i
        out=$(basename ${array[$i]})
        echo blastp -outfmt 6 -db singledb/db -query ${array[$i]}/all_protein.fa -out rp_blast_results/${out}.csv -evalue 10e-3 -max_target_seqs 10000 -num_threads 16
    fi
done

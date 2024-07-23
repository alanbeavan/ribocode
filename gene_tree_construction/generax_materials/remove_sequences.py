#!/usr/bin/env python3.6
"""Remove all sequences from a fasta alignment that have over a user given threshold % gaps."""

import sys
import my_module as mod

def get_args():
    """Get user arguments."""
    if len(sys.argv) == 4:
        return sys.argv[1:]
    print("USAGE: python3 %gap_threshold infile outfile")
    sys.exit()

def main():
    """Do the things."""
    threshold, infile, outfile = get_args()
    if "." in threshold:
        threshold = float(threshold)
    else:
        threshold = int(threshold)
    seqs = mod.read_fasta(infile)
    total_len = 0
    new_seqs = {}
    for name, seq in seqs.items():
        if total_len == 0:
            total_len = len(seq)
        if seq.count("-") < total_len * threshold / 100: 
            new_seqs[name] = seq
    with open(outfile, "w", encoding = "utf8") as out:
        for key, value in new_seqs.items():
            out.write(">" + key + "\n" + value + "\n")




if __name__ == "__main__":
    main()

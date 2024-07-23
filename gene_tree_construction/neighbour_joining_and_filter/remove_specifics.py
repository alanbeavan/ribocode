#!/usr/bin/env python3.6
"""Docstring."""

import glob
import my_module as mod

def main():
    """Do the things."""
    to_remove = mod.get_file_data("list_of_long_proteins_to_remove")
    for filename in glob.glob("iqtree_runs/*/aln.aln.fa.before_removal"):
        seqs = mod.read_fasta(filename)
        new_seqs = {}
        for key, value in seqs.items():
            if key not in to_remove:
                new_seqs[key] = value
        print(filename + "\t" + str(len(seqs)) + "\t" + str(len(new_seqs)))
        newname = ".".join(filename.split(".")[:-1])
        with open(newname, "w", encoding = "utf8") as out:
            for key, value in new_seqs.items():
                out.write(">" + key + "\n" + value + "\n")


if __name__ == "__main__":
    main()

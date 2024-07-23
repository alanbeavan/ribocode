#!/usr/bin/env python3.6
"""Docstring."""

import glob
import my_module as mod

def main():
    """Do the things."""
    files = glob.glob("default_fams/*")
    groups = mod.get_file_data("50_overlap_groups.csv")
    big_seqs = {}
    names = {}
    i = 0
    done = []
    for group in groups[1:]:
        genes = group.split(",")
        combi_seqs = {}
        for gene in genes:
            seqs = mod.read_fasta("default_fams/" + gene + ".fa")
            done.append("default_fams/" + gene + ".fa")
            combi_seqs.update(seqs)
        big_seqs["group_" + str(i)] = combi_seqs
        names["group_" + str(i)] = ",".join(genes)
        i += 1

    for filename in files:
        if filename not in done:
            big_seqs["group_" + str(i)] = mod.read_fasta(filename)
            print(i)
            print(filename)
            print(len(big_seqs["group_" + str(i)]))
            #print(big_seqs["group_" + str(i)])
            names["group_" + str(i)] = filename.split("/")[1].split(".")[0]
            i += 1
    for name, seqs in big_seqs.items():
        with open("merged_by_50/" + name + ".fa", "w", encoding = "utf8") as out:
            print(name)
            print(len(seqs))
            for key, value in seqs.items():
                out.write(">" + key + "\n" + value + "\n")

    with open("merged_by_50_names.csv", "w", encoding = "utf8") as out:
        out.write("name\tgenes\n")
        for key, value in names.items():
            out.write(key + "\t" + value + "\n")


if __name__ == "__main__":
    main()

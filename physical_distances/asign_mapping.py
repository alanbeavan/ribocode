#!/usr/bin/env python3
"""Docstring."""

import my_module as mod

def main():
    """Do the things."""
    riboseqs = mod.read_fasta("pymol_seqs.fa")
    homoseqs = mod.read_fasta("homo_rps.fa")
    clade_rates = mod.get_file_data("dup_counts_clades_new.tsv")
    mapping = {}
    for key, value in riboseqs.items():
        for key1, value1 in homoseqs.items():
            if value == value1:
                mapping[key] = key1.split("_")[0]
                break
        if key not in mapping:
            print(key)
            print("MEGAPROBLEM MEGAPROBLEM. MICE FLIES AND SPIDERS FLICE MIDERS AND SPIES")
            if key == "4UG0_SM":
                mapping[key] = "RPS12"

    fungi_rates = {}
    for line in clade_rates:
        if "plant" in line:
            fields = line.split()
            name_list = fields[0].split("...")
            current = "agedebagedboobaahbingbong"
            for name in name_list:
                if name.startswith("group"):
                    name = "_".join(name.split("_")[2:])
                if name.startswith("RP") and len(name) < len(current):
                    current = name
            fungi_rates[current] = fields[2]

    with open("mapping_plant", "w") as out:
        for key, value in mapping.items():
            print(value)
            out.write(key + "\t" + value + "\t" + fungi_rates[value] + "\n")

    to_check = []
    for key in homoseqs.keys():
        if key.split("_")[0] not in to_check:
            to_check.append(key.split("_")[0])
    
    done = list(mapping.values())
    for apple in to_check:
        if apple not in done:
            print(apple)


if __name__ == "__main__":
    main()

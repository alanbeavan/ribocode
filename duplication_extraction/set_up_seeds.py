#!/usr/bin/env python3.6
"""Docstring."""

import string
import my_module as mod

def main():
    """Do the things."""
    seed_info = mod.get_file_data("../after_ptp/locations_with_combo.csv")
    locs = {}
    for line in seed_info:
        fields = line.split()
        locs["____".join(fields[:2])] = fields[2]
    
    
    families = []
    alignments = {}
    filtered = {}
    cur_fam = ""
    for line in mod.get_file_data("generax_RP_only_starting_trees_lcp_from_headers.families"):
        if line.startswith("-"):
            families.append(line[1:])
            cur_fam = line[1:]
        elif line.startswith("ali"):
            alignments[cur_fam] = "/".join(line.split(" = ")[1].split("/")[:-1]) + "/aln.fa.longest_peptides_from_headers.fa.smaller"
            filtered[cur_fam] = "/".join(line.split(" = ")[1].split("/")[:-1]) + "/aln.aln.fa.longest_peptides_from_headers.smaller.trimmed.gt50.filtered"

    table = ["family\theaders"]
    for family in families:
        seqs = mod.read_fasta(alignments[family])
        seqs2 = mod.read_fasta(filtered[family])
        for key, value in seqs.items():
            if value[-1] == "*":
                seqs[key] = value[:-1]
        seed_names = []
        fields =  family.split("_")
        group = "_".join(fields[:2])
        rest = "_".join(fields[2:])
        sub_fams = rest.split("...")
        for fam in sub_fams:
            for key in locs:
                if key.split("____")[0] == group and key.split("____")[1] == fam:
                    for key, value in mod.read_fasta(locs[group + "____" + fam]).items():
                        #ok I'm going to have to get the sequence rather than the name then get all the names with such a sequence. pfft
                        if value[-1] == "*":
                            value = value[:-1]
                        for key2, value2 in seqs.items():
                            if value == value2 and key2 in seqs2:
                                to_add = ""
                                flag = 0
                                flag1 = 0
                                #print(key2)
                                #for char in key2:
                                #    if char == "." and flag1 == 0:
                                #        to_add = to_add + "_"
                                #        flag1 = 1
                                #    elif char == "_" and flag == 1:
                                #        to_add = to_add + "_"
                                #    elif char == "_":
                                #        to_add = to_add + "."
                                #        flag = 1
                                #    else:
                                #        to_add = to_add + char
                                #to_add = key2.translate(str.maketrans("_", "."))
                                #to_add = to_add.translate(str.maketrans("|", "_"))
                                to_add = key2
                                if not to_add in seed_names:
                                    seed_names.append(to_add)
        print(len(seed_names))
        table.append(family + "\t" + ",".join(seed_names))
    with open("seed_names.csv", "w", encoding = "utf8") as out:
        out.write("\n".join(table) + "\n")


                    




if __name__ == "__main__":
    main()

#!/usr/bin/env python3.6
"""
For a given set of species and gene family, extract the number of duplications
and losses that occured in that clade of the species tree.
"""

import ete3
import sys
import my_module as mod

def get_args():
    """user arguments."""
    if not len(sys.argv) == 4:
        print("USAGE: python3 extract_duplication_rates.py gene_tree_file species_list_file separator")
        sys.exit()
    return sys.argv[1:]

def main():
    """Do the things."""
    treefile, sp_list, sep = get_args()
    species = mod.get_file_data(sp_list)
    dups = 0
    done = []
    for node in ete3.Tree(treefile, format = 1).traverse():
        flag = 1
        for leaf in node:
            if leaf.name.split(sep)[0] not in species:
                flag = 0
                break
            if leaf.name in done:
                flag = 0
                break
        if flag:
            #count the duplications
            for subnode in node.traverse():
                if subnode.name == "D":
                    dups += 1
                elif subnode.name != "S":
                    if subnode.name not in done:
                        done.append(subnode.name)
    print(dups)





if __name__ == "__main__":
    main()

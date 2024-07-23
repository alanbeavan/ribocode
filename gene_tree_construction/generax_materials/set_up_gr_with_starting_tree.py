#!/usr/bin/env python3.6
"""Docstring."""

import my_module as mod

def main():
    """Do the things."""
    family_lines = mod.get_file_data("generax_rp_only_smaller.families")
    newlines = []
    for line in family_lines:
        newlines.append(line)
        if line.startswith("ali"):
            treefile = line.split(" = ")[1][:-9] + ".treefile"
            treestring = mod.get_file_data(treefile)[0]
            treestring = treestring.translate(str.maketrans("_", "."))
            treestring = treestring.translate(str.maketrans("|", "_"))
            with open(line.split(" = ")[1] + ".treefile", "w", encoding = "utf8") as out:
                out.write(treestring + "\n")
            newlines.append("starting_gene_tree = " + line.split(" = ")[1] + ".treefile")
    with open("generax_RP_only_starting_trees.families", "w", encoding = "utf8") as out:
        out.write("\n".join(newlines) + "\n")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Docstring."""

import my_module as mod

def main():
    """Do the things."""
    command_lines = []
    for line in mod.get_file_data("mapping_with_colour_plant")[1:]:
        fields = line.split(",")
        chain = fields[1] #<- this will usually work I think, but for the yeast chromosome, the chains in the file are off due to annoyances
        chain = ""
        if line.startswith("8cgn") or line.startswith("4v7e"):
            for line2 in mod.get_file_data("pdb_chain_dictionary_full.csv"):
                if fields[0].upper() in line2 and line2.endswith(fields[2]):
                    prot_name = line2.split("\t")[2]
                    break
            for line2 in mod.get_file_data("distances_from_Bulat/arabidopsis/chain_info/4v7e")[3:]:
                fields2 = line2.split("\t")
                if prot_name in fields2:
                    chain = "Chain " + line2.split("\t")[0]
        command_lines.append("select " + chain)
        command_lines.append("color 0x" + fields[4][1:] + ", (sele)")
    with open("commands_plant.txt", "w", encoding = "utf8") as out:
        out.write("\n".join(command_lines) + "\n")

if __name__ == "__main__":
    main()

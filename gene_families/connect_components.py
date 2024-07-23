#!/usr/bin/env python3
"""Docstring."""

import my_module as mod

def main():
    """Do the things."""
    lines = mod.get_file_data("50_and_over.csv")
    groups = []
    for line in lines:
        fields = line.split(",")
        flag = 0 
        for group in groups:
            if fields[0] in group and fields[1] in group:
                flag = 1
                break
            elif fields[0] in group:
                flag = 1
                group.append(fields[1])
            elif fields[1] in group:
                flag = 1
                group.append(fields[0])
        if not flag:
            groups.append([fields[0], fields[1]])
    with open("50_overlap_groups.csv", "w", encoding = "utf8") as out:
        for group in groups:
            out.write(",".join(group) + "\n")

if __name__ == "__main__":
    main()

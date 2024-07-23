#!/usr/bin/env python3.6
"""
From phylotreepruner_results:
    get a list of subclades containing the seed sequences.
    find the smallest subclade that contains all of these.
    If it's less than, say, 2000 sequences, take the smallest subclade that features these subclades that is >2000 sequences

For some families, there will be more than one set of seed seqs. Run this on each and if the same tree comes out at the end, they should be treated the same. Otherwise, if completely independent, that's 2 different families. Otherwise, if there is some overlap, they maybe need to be joined.
"""
import sys
import os
from ete3 import Tree
import my_module as mod

def get_args():
    """You know."""
    if len(sys.argv) != 2:
        print("USAGE: python3 extract_clade.py group_n")
    return sys.argv[1]

def shave_seq(seq):
    """Just get rid of all the non-alpha characters."""
    new_seq = ""
    for char in seq:
        if char.isalpha():
            new_seq = new_seq + char
    return new_seq

def write_results(group, gene, tree, aln):
    """Write the results."""
    if not os.path.exists(group + "_" + gene  + "_midpoint_rooted"): 
        os.makedirs(group + "_" + gene + "_midpoint_rooted")
    tree.write(outfile = group + "_" + gene + "_midpoint_rooted/tree.nwk")
    with open(group + "_" + gene + "_midpoint_rooted/aln.nwk", "w", encoding = "utf8") as out:
        for key, value in aln.items():
            out.write(">" + key + "\n" + value + "\n")

def main():
    """
    First we only need to deal with families of size 2000 or above
    For each gene:
        find the seed sequences in the tree
        find the smallest clade that includes all the seed sequences.
            if it's 2000 or less, keep moving back a node until it is size 2000
            if it's 2000 or more, this is your clade
        write the alignment and tree to a file in a directory
    I guess if a gene family is still over, say, 4000 sequences, we will need to make a note of that and investigate further
    """
    group_n = get_args()
    for line in mod.get_file_data("locations.csv"):
        group, gene_fam, queries_file = line.split()
        if group == "group_" + group_n:
            print(line)

            #get the query seqs
            queries = mod.read_fasta(queries_file)
            for key, value in queries.items():
                queries[key] = shave_seq(value)
 
            #get the seqs in the tree
            tree = Tree("../../src_and_wrapper_scripts/" + group + "/tree_modified_names.nwk")
            tree.set_outgroup(tree.get_midpoint_outgroup())
            aln = mod.read_fasta("../../src_and_wrapper_scripts/" + group + "/full_alignment_modified_names.fa")
            aln_mod = {}
            for key, value in aln.items():
                aln_mod[key] = shave_seq(value)
            if len(aln) <= 2000:
                print("length of initial alignment less than 2000 seqs")
                write_results(group, gene_fam, tree, aln_mod)
                continue

            #find the names of the sequences with the same sequence as the queries
            targets = []
            for seq in queries.values():
                for key, value in aln_mod.items():
                    if value == seq:
                        targets.append(key)
            print(targets)

            #read in the tree and begin traversal
            if len(targets) == 1:
                current_node = tree.search_nodes(name = targets[0])[0]
            elif len(targets) == 0:
                #problemos
                with open("problems_" + group + ".csv", "a", encoding = "utf8") as out:
                    out.write(line + "\n")
                #get the best blast hit
                file_bits = queries_file.split("/")
                blast_results = "/".join(file_bits[:2]) + "/ribo-interactome_blast_results/" + file_bits[-1] + ".csv"
                best_hit = mod.get_file_data(blast_results)[0].split()[1]
                name_fields = best_hit.split("_")
                best_hit = "_".join(name_fields[:2]) + "|" + "_".join(name_fields[2:])
                print(best_hit)
                current_node = tree.search_nodes(name = best_hit)[0]
            else:
                current_node = tree.get_common_ancestor(targets)

            n_tips = 0
            for leaf in current_node:
                n_tips += 1
            print(n_tips)
            while n_tips <= 2000:
                backup_node = current_node
                if current_node.is_root():
                    if n_tips >= 6000:
                        current_node = backup_node
                    break
                else:
                    current_node = current_node.up
                    n_tips = 0
                    for leaf in current_node:
                        n_tips += 1
                    print(n_tips)
                    if n_tips >= 6000:
                        current_node = backup_node
                        break
            
            #filter aln
            new_aln = {}
            for key, value in aln.items():
                for leaf in current_node:
                    if leaf == key:
                        new_aln[key] = shave_seq(value)

            #write_results
            write_results(group, gene_fam, current_node, new_aln)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3.6
"""
From generax output
1.  extract each clade emerging from a duplciation at the root of the species
    tree. 
2.  Find the clade that contains all the seed sequences for the family
3.  Prune the gene tree so that it contains only the sequences from that clade
4.  Put all this in a format for generax including the families file
"""
import os
import ete3
import glob
import sys
import my_module as mod

def get_args():
    """Get user arguments, printing usage if wrongly supplied."""
    if len(sys.argv) != 5:
        print("USAGE: python3 extract_orthologs.py generax_directory\
 seeds_file output_directory generax_family_file")
        sys.exit()
    return sys.argv[1:]

def main():
    """Do the things."""
    indir, seeds_file, outdir, generax_file = get_args()
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    if not os.path.exists(outdir + "/true_orthologs"):
        os.makedirs(outdir + "/true_orthologs")
    if not os.path.exists(outdir + "/ortho_alignments"):
        os.makedirs(outdir + "/ortho_alignments")
    if not os.path.exists(outdir + "/split_into_orthogroups"):
        os.makedirs(outdir + "/split_into_orthogroups")
 
    
    #prepare the seeds seqs
    seeds = {}
    for line in mod.get_file_data(seeds_file):
        seeds[line.split("\t")[0]] = line.split("\t")[1].split(",")
    
    alignments = {}
    cur_fam = ""
    for line in mod.get_file_data(generax_file):
        if line.startswith("-"):
            cur_fam = line[1:]
        elif line.startswith("ali"):
            alignments[cur_fam] = line.split(" = ")[1]

    gene_trees = glob.glob(indir + "/results/*/*newick")
    for results in gene_trees:
        #read in trees
        family = results.split("/")[-2]
        print(family)
        tree = ete3.Tree(results)
        reconciled_tree = ete3.Tree(indir + "/reconciliations/" + family + "_events.newick", format = 1)

        #traverse tree to exctract orthogroups.
        #while root is labeled "D" and tree has tips(?), find the first "S"
            #label and take this as the root of the nth orthogroup, save that
            #and remove it (node.detach) and its daughter also remove branches with only 1
            #daughter, joining that daughter to the previous branch (how?)
        orthotrees = []
        tracker = 1.1
        backup_tree = reconciled_tree.copy()
        while reconciled_tree.name == "D":
            if tracker == len(reconciled_tree):
                break
            tracker = len(reconciled_tree)
            for node in reconciled_tree.get_descendants("levelorder"):
                if len(node.children) == 1:
                    print("ccollapsing double branch")
                    node.delete()
                if node.name == "S" and len(node.children) == 2:
                    #prune and save
                    orthotrees.append(node.detach())
                    print("pruning")
                    break
            if len(reconciled_tree.children) != 2:
                print("removing null root")
                reconciled_tree = reconciled_tree.children[0]
        orthotrees.append(reconciled_tree)


        #write all of those to a nested tructure
        print(len(orthotrees))
        if not os.path.exists(outdir + "/split_into_orthogroups/" + family):
            os.makedirs(outdir + "/split_into_orthogroups/" + family)

        for i in range(len(orthotrees)):
            orthotrees[i].write(format = 1, outfile = outdir + "/split_into_orthogroups/" + family + "/group" + str(i) + ".nwk")


        #now identify the orthogroup with all the starget sequences in.
        to_find = seeds[family]
        orthodone = 0
        #If they're all in one orthogroup, just return that.
        #Otherwise get the node that is the last common ancestor of the seeds.
        for i in range(len(orthotrees)):
            tips = orthotrees[i].iter_leaves()
            tipnames = []
            for tip in tips:
                tipnames.append(tip.name)
            in_tree = 0
            for value in to_find:
                if value in tipnames:
                    in_tree += 1
            print(in_tree)
            if in_tree == len(to_find):
                #write the tree
                orthotrees[i].write(format = 1, outfile = outdir + "/true_orthologs/" + family + ".true_orthologs_s.nwk")
                print(family + " all seeds contained in 1 orthogroup. Done")
                orthodone = 1
                break
        leaves = []
        for name in to_find:
            print(name)
            leaves.append(backup_tree.search_nodes(name=name)[0])
        if not orthodone:
            print(family + " seeds split into paralogs. Using common Ancestor. Done")
            reconciled_tree.get_common_ancestor(leaves).write(format = 1, outfile = outdir + "/true_orthologs/" + family + ".true_orthologs_d.nwk")
            tipnames = []
            for tip in reconciled_tree.get_common_ancestor(leaves).iter_leaves():
                tipnames.append(tip.name)

        #make the reduced alignment
        ali = mod.read_fasta(alignments[family])
        reduced_ali = {}
        for tipname in tipnames:
            reduced_ali[tipname] = ali[tipname]
        with open(outdir + "/ortho_alignments/" + family + ".fa", "w", encoding = "utf8") as out:
             for key, value in reduced_ali.items():
                 out.write(">" + key + "\n" + value + "\n")
        

        


if __name__ == "__main__":
    main()

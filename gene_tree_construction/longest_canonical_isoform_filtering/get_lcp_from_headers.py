#!/usr/bin/env python3.6
"""Take the longest canonical peptide from each gene in an alignment given the information contained in the headers."""

import glob
import re
import my_module as mod

def main():
    """Do the things."""
    prot_to_gene = {}
    prot_lengths = {}
    for line in mod.get_file_data("protein_gene_table.csv")[1:]:
        #example header
        #Mus_musculus|ENSMUSP00000034740.8
        fields = line.split("\t")
        prot_to_gene[fields[0] + "|" + "_colon_".join(fields[1].split()[0].split(":"))] = fields[0] + "_" + fields[3]
        prot_lengths[fields[0] + "|" + "_colon_".join(fields[1].split()[0].split(":"))] = int(fields[4])

    for seq_file in glob.glob("alignments/*/aln.fa"):
    #for seq_file in ["alignments/group_123_60S_ribosomal_protein_L7-like_1...60S_ribosomal_protein_L7...P32100...Q9VKC1...RPL7/aln.fa"]:
        new_seqs = {}
        genes = {}
        seqs = mod.read_fasta(seq_file)
        prot_headers = list(seqs.keys())
        for header in prot_headers:
            if not header.startswith("Hordeum_vulgare"):
                header = re.sub("_sp\.\|", "_sp|", header)
                if prot_to_gene[header] not in genes:
                    genes[prot_to_gene[header]] = header
                    print(header + " added as first for gene")
                elif prot_lengths[header] > prot_lengths[genes[prot_to_gene[header]]]:
                    print(genes[prot_to_gene[header]] + " removed and replaced with " +header)
                    genes[prot_to_gene[header]] = header
                else:
                    print(header + " not added because its gene is already in with a longer protein")
        to_keep = list(genes.values())
        for key, value in mod.read_fasta(seq_file).items():
            key = "_colon_".join(key.split()[0].split(":"))
            key = re.sub("_sp\.\|", "_sp|", key)

            print(key)
            if key in to_keep:
                key = re.sub("_", ".", key)
                key = re.sub("Adiantum.capillus-veneris", "Adiantum.capillus.veneris", key)
                key = re.sub("\|", "_", key, count = 1)
                print("changed to " + key + "and kept")
                #print("kept")
                new_seqs[key] = value
            else:
                print("chucked")
                
        with open(seq_file + ".longest_peptides_from_headers.fa", "w", encoding = "utf8") as out:
            for key, value in new_seqs.items():
                out.write(">" + key + "\n" + value + "\n")
                



if __name__ == "__main__":
    main()

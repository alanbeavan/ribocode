#!/usr/bin/env python3
"""
Output will be a table with fields as species, protein, gene, geneid, prot_length.
"""

import random
import re
import glob
import my_module as mod

def main():
    """Do the things."""
    #with open("protein_gen_table.csv", "a", encoding = "utf8") as out:
        #out.write("species,protein_header,cds_header,geneid,prot_length\n")
    #cds = {}
    ensembl = glob.glob("ensembl_downloads/ensembl_genomes/*/*cds.all.fa")
    ncbi = glob.glob("ncbi_downloads/ncbi_dataset/data/GC*/*cds.fa")
    #lines = mod.get_file_data("protein_gene_table.csv")

    species_done = mod.get_file_data("species_done")
    #for line in lines:
    #    species_done.append(line.split("\t")[0])
    random.shuffle(ensembl)
    #proteins = mod.read_fasta("all_proteins.fa")
    for genome in ensembl:
    #for genome in list(reversed(ensembl)):
        table_lines = []
    #for genome in ["ensembl_downloads/ensembl_genomes/corymbia_citriodora/Corymbia_citriodora.Ccitriodora_v2_1.pep.all.fa"]:
    #for genome in ["ensembl_downloads/ensembl_genomes/cannabis_sativa/Cannabis_sativa_female.cs10.cds.all.fa"]:
        cds = []
        species = genome.split("/")[2]
        if species in species_done:
            print(species + " done")
        if species not in species_done:
            print(species)
            #cds[species] = []
            for line in mod.get_file_data(genome):
                if line.startswith(">"):
                    #cds[species].append(line[1:])
                    cds.append(line[1:])
            for key, value in mod.read_fasta(genome[:-10] + "pep.all.fa").items():
                p_len = len(value)
                geneid = key.split("gene:")[1].split()[0]
                transcript = key.split("transcript:")[1].split()[0]
                reg = re.compile(re.escape(transcript + " "))
                cds_header = list(filter(reg.search, cds))
                if len(cds_header) != 1:
                    print(cds_header)
                    exit()
                table_lines.append(species + "\t" + key + "\t" + cds_header[0] + "\t" + geneid + "\t" + str(p_len))
            with open("protein_gen_table.csv", "a", encoding = "utf8") as out:
                out.write("\n".join(table_lines) + "\n")

#    random.shuffle(ncbi)
#    for genome in ncbi:
#        species = "_".join(mod.get_file_data(genome[:-6] + "pep.fa")[0].split("[")[-1][:-1].split()[:2])
#        table_lines = []
#        if species not in species_done:
#            print(species)
#            if species.endswith("."):
#                species = species[:-1]
#            cds = []
#            for line in mod.get_file_data(genome):
#                if line.startswith(">"):
#                    cds.append(line[1:])
#            for key, value in mod.read_fasta(genome[:-6] + "pep.fa").items():
#                p_len = len(value)
#                protein_id = key.split()[0]
#                reg = re.compile(protein_id)
#                cds_header = list(filter(reg.search, cds))
#                if len(cds_header) != 1:
#                    print(cds_header)
#                geneid = cds_header[0].split("[")[1].split("]")[0].split("=")[1]
#                table_lines.append(species + "\t" + key + "\t" + cds_header[0] + "\t" + geneid + "\t" + str(p_len))
#            with open("protein_gene_table.csv", "a", encoding = "utf8") as out:
#                out.write("\n".join(table_lines) + "\n")
    

        



if __name__ == "__main__":
    main()

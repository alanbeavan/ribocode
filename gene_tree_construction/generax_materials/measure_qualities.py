#!/usr/bin/env python3.6
"""
Output will be a table with the gene family, lenght for original, gt_trimmed,
gappyout_trimmed, mean gtscore for the original, gt_trimmed, gappyout_trimmed,
mean sscore for original, gt_trimmed, gappyout_trimmed.
"""

import glob
import my_module as mod

def main():
    """Do the things."""
    table = ["family,length_orig,length_gt,length_gappyout,gtscore_orig,gt_score_gt,gt_score_gappyout,sscore_orig,sscore_gt,sscore_gappyout"]
    for loc in glob.glob("alignments/*"):
        line = [loc.split("/")[1]]
        for ending in ["", ".trimmed.gt50.filtered", ".trimmed.gappyout.filtered"]:
            seqs = mod.read_fasta(loc + "/aln.aln.fa.longest_peptides" + ending)
            for value in seqs.values():
                line.append(str(len(value)))
                break
        for ending in [".gtscores", ".trimmed.gt50.filtered.gtscores", ".trimmed.gappyout.filtered.gtscores"]:
            scores = mod.get_file_data(loc + "/aln.aln.fa.longest_peptides" + ending)[3:]
            vals = []
            for score in scores:
                vals.append(float(score.split()[2]))
            line.append(str(sum(vals)/len(vals)))

        for ending in [".sscores", ".trimmed.gt50.filtered.sscores", ".trimmed.gappyout.filtered.sscores"]:
            scores = mod.get_file_data(loc + "/aln.aln.fa.longest_peptides" + ending)[3:]
            vals = []
            for score in scores:
                vals.append(float(score.split()[1]))
                if float(score.split()[1]) > 1:
                    print("/aln.aln.fa.longest_peptides" + ending)
                    print(score)
                    exit()
            line.append(str(sum(vals)/len(vals)))

        table.append(",".join(line))
    with open("alignment_scores.csv", "w", encoding = "utf8") as out:
        out.write("\n".join(table) + "\n")

if __name__ == "__main__":
    main()

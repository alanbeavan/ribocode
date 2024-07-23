scores = read.csv("alignment_scores.csv")

#lengths
boxplot(scores$length_orig, scores$length_gt, scores$length_gappyout, names= c("original", "50% gap removed", "gappyout"), ylab = "alignment length")
boxplot(scores$length_gt, scores$length_gappyout, names = c("50% gap removed", "gappyout"), ylab = "alignment length")
length_diff = scores$length_gt - scores$length_gappyout
rel_length_diff = (scores$length_gt - scores$length_gappyout) / pmin(scores$length_gt, scores$length_gappyout)
hist(length_diff, xlab = "length of gt50 - length of gappyout")
hist(rel_length_diff, xlab = "length of gt50 - length of gappyout / the minumum length of these", xlim = c(-20, 20), breaks = 100)
boxplot(length_diff)
boxplot(rel_length_diff)
boxplot(rel_length_diff)
scores[which(scores$length_gt-scores$length_gappyout < -1000),]
scores[which(rel_length_diff > 10 | rel_length_diff < -10),]
t.test(scores$length_gappyout, scores$length_gt, alternative="two.sided")
t.test(scores$length_gappyout, scores$length_gt, alternative="less")

#gap scores
boxplot(scores$gtscore_orig, scores$gt_score_gt, scores$gt_score_gappyout, names = c("original", "50% gap removed", "gappyout"), ylab = "gap score")


#similarity scores
boxplot(scores$sscore_orig, scores$sscore_gt, scores$sscore_gappyout, names = c("original", "50% gap removed", "gappyout"), ylab = "similarity score")
boxplot(scores$sscore_gt, scores$sscore_gappyout, names = c("50% gap removed", "gappyout"), ylab = "similarity score")
scores[which(scores$sscore_gt < 0.01),]
improvement_gt = scores$sscore_gt - scores$sscore_orig
improvement_gappy = scores$sscore_gappyout - scores$sscore_orig
boxplot(improvement_gt, improvement_gappy, names = c("50% gap removed", "gappyout"), ylab = "improvement in similarity score")

boxplot(scores$sscore_gt - scores$sscore_gappyout, ylab = "similarity score gt50 - similarity score gappyout")
length((scores$sscore_gt - scores$sscore_gappyout)[(scores$sscore_gt - scores$sscore_gappyout) < 0])
length((scores$sscore_gt - scores$sscore_gappyout)[(scores$sscore_gt - scores$sscore_gappyout) >0])
scores[which(improvement_gappy < 0 | improvement_gt < 0),]
t.test(scores$sscore_orig, scores$sscore_gt, paired=TRUE, alternative="less")
t.test(scores$sscore_orig, scores$sscore_gappyout, paired=TRUE, alternative="less")
t.test(scores$sscore_gt, scores$sscore_gappyout, paired=TRUE, alternative="less")


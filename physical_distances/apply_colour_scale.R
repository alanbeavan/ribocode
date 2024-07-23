

mapping = read.csv("distances_total_for_stats.csv", na.strings=c("NA"))
to_include = read.table("mapping_animal")
#scale_colour_continuous(mapping$V3)
#1100ff
#ffa500



#fungi - 8cgn
#plant - 4v7e
#to_include = mapping[which(mapping$ribosome == "8cgn"),]
to_include = mapping[which(mapping$ribosome == "4v7e"),]

high = max(to_include$plant_dups, na.rm=TRUE)
low = min(to_include$plant_dups, na.rm=TRUE)
high = max(to_include$V3)
low = min(to_include$V3)
#pal <- colorRamp(c("red", "blue"))
#pal(0.5)
#scale = pal(seq(0, 1, len = high - low + 1))

pal <- colorRampPalette(c("purple", "blue", "green", "yellow", "orange", "red"))
pal <- colorRampPalette(c("blue", "yellow", "red"))
pal <- colorRampPalette(c("blue", "orange"))
scale = pal(high - low + 1)


col_vals = c()
i=0
for(value in to_include$V3) {
  col_vals = c(col_vals, scale[value-low+1])
}
col_vals
with_colour = cbind(to_include[,c(1,2,4,11)], col_vals)
names(with_colour) <- c("pdb_name", "chain_name", "RP_name", "dups_plant", "colour_plant")
write.csv(file = "mapping_with_colour_plant", with_colour, quote=F, row.names=F)

plot(col_vals)
plot(to_include$V3, col = col_vals)
legend(x = 60, y = 100, legend = to_include$V3, col = col_vals)


library(ggplot2)
library(gcookbook)  # Load gcookbook for the heightweight data set

# Create the base plot
hw_plot <- ggplot(heightweight, aes(x = ageYear, y = heightIn, colour = weightLb)) +
  geom_point(size = 3)

hw_plot

# A gradient with a white midpoint
library(scales)
hw_plot +
  scale_colour_gradient2(
    low = muted("red"),
    mid = "white",
    high = muted("blue"),
    midpoint = 110
  )

# With a gradient between two colors (black and white)
hw_plot +
  scale_colour_gradient(low = "blue", high = "orange",
                        labels = c("0", "", "", "",  "", "22"))

# A gradient of n colors
hw_plot +
  scale_colour_gradientn(colours = c("darkred", "orange", "yellow", "white"))


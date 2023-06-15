library(dplyr)
library(data.table)
library(ggplot2)

data <- fread("")

ggplot(data %>% filter(distance<0.9),aes(x=distance)) +
  geom_histogram(bins = 100)



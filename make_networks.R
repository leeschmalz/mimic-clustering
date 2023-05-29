library(data.table)
library(dplyr)

data <- fread("/Users/leeschmalz/Documents/GitHub/mimicPatientClustering/distance_matrix_mst.csv") %>% 
  rename(Source=hadm1, Target=hadm2)

for(distance_cut in c(0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75)){
  print(distance_cut)
  mst <- data %>% filter(mst)
  non_mst <- data %>% filter(!mst) %>% filter(distance < distance_cut)
  
  network <- rbind(mst,non_mst)
  
  fwrite(network,paste0("/Users/leeschmalz/Documents/GitHub/mimicPatientClustering/networks/network_",distance_cut,".csv"))
}
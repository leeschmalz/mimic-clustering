from similarity import make_list_of_possible_edges
from distance import similarity_to_distance
from graph import make_minimum_spanning_tree
import pandas as pd

#mimic
df = pd.read_csv('./DIAGNOSES_ICD.csv')

similarity = make_list_of_possible_edges(df, condition='all') # 99591 is sepsis
distance = similarity_to_distance(similarity)

# Save the distance matrix to a csv file
distance.to_csv('./output/data/distance_matrix.csv', index=False)

_, distance = make_minimum_spanning_tree(distance)
distance.to_csv('./output/data/distance_matrix_mst.csv', index=False)

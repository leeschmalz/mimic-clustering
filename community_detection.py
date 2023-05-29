from cdlib import algorithms
import networkx as nx
import pandas as pd
import colorsys

cutoff = 0.55

data = pd.read_csv('./distance_matrix_mst.csv')
data['hadm1'] = data.hadm1.astype(str)
data['hadm2'] = data.hadm2.astype(str)

# filter out edges with distance > cutoff and not in mst
data = data[(data.distance <= cutoff) | (data.mst == True)]

# create graph
G = nx.from_pandas_edgelist(data, 'hadm1', 'hadm2', edge_attr='distance')
# make louvian community detection
communities = algorithms.louvain(G, weight='distance')

community_mapping = {}
for i, community in enumerate(communities.communities):
    for node in community:
        community_mapping[node] = i

metadata = pd.DataFrame(list(community_mapping.items()), columns=['id', 'community'])

num_communities = len(communities.communities)
colors = [colorsys.hsv_to_rgb(i/num_communities, 1, 1) for i in range(num_communities)]
hex_colors = [f"#{int(r*255):02X}{int(g*255):02X}{int(b*255):02X}" for r, g, b in colors]

metadata['color'] = metadata['community'].map(lambda c: hex_colors[c])

data.to_csv('./network_' + str(cutoff) + '.csv', index=False)
metadata.to_csv('./network_' + str(cutoff) + '_meta.csv', index=False)
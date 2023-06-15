from cdlib import algorithms
import networkx as nx
import pandas as pd
import colorsys

cutoff = 0.4

data = pd.read_csv('')
data['hadm1'] = data.hadm1.astype(str)
data['hadm2'] = data.hadm2.astype(str)

# filter out edges with distance > cutoff and not in mst
data = data[(data.distance <= cutoff) | (data.mst == True)]

# create graph
G = nx.from_pandas_edgelist(data, 'hadm1', 'hadm2', edge_attr='distance')
# make louvian community detection
print('Making louvian communities...')
communities = algorithms.louvain(G, weight='distance')
print(f'Found {len(communities.communities)} communities.')

community_mapping = {}
for i, community in enumerate(communities.communities):
    for node in community:
        community_mapping[node] = i

metadata = pd.DataFrame(list(community_mapping.items()), columns=['id', 'community'])

# Get the top n most frequent communities
n=15
top_n_communities = metadata['community'].value_counts().nlargest(n).index

num_communities = len(communities.communities)
colors = [colorsys.hsv_to_rgb(i/n, 1, 1) for i in range(n)]
hex_colors = [f"#{int(r*255):02X}{int(g*255):02X}{int(b*255):02X}" for r, g, b in colors]

# Assign colors to the top n communities
metadata.loc[metadata['community'].isin(top_n_communities), 'color'] = metadata.loc[metadata['community'].isin(top_n_communities), 'community'].map(lambda c: hex_colors[c])

# Assign gray color to the rest of the communities
metadata.loc[~metadata['community'].isin(top_n_communities), 'color'] = '#808080'  # Gray color

data.to_csv('./networks/' + str(cutoff) + '.csv', index=False)
metadata.to_csv('./networks/' + str(cutoff) + '_meta.csv', index=False)
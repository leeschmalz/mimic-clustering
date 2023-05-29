def make_minimum_spanning_tree(distance_matrix):

    from tqdm import tqdm # pip3 install tqdm

    '''
    input: distance matrix: 'hadm1', 'hadm2', 'distance'
    output: minimum spanning tree: 'hadm1', 'hadm2', 'distance', 'mst'

    Adds a column to distance matrix indicating whether edge is in minimum spanning tree. Uses Kruskal's algorithm.
    '''
    
    hadm_list = list(set(list(distance_matrix.hadm1) + list(distance_matrix.hadm2)))

    class MST:
        def __init__(self, hadm_list):
            self.nodes = { hadm: None for hadm in hadm_list }
            self.groups = {0:[]}
            self.edges = []

    mst = MST(hadm_list=hadm_list)

    # sort edges by distance
    distance_matrix = distance_matrix.sort_values(by='distance')

    for i in tqdm(range(len(distance_matrix))):
        node1 = distance_matrix.iloc[i].hadm1
        node2 = distance_matrix.iloc[i].hadm2
        distance1 = distance_matrix.iloc[i].distance
        
        # both nodes are already in the tree in the same group -> skip as this would create a cycle
        if (mst.nodes[node1] != None) and (mst.nodes[node1] == mst.nodes[node2]):
            continue

        # neither node is in the tree -> add edge to tree in a new group
        elif (mst.nodes[node1] == None) and (mst.nodes[node2] == None):
            mst.edges.append((node1, node2))

            new_group = max(mst.groups.keys()) + 1
            mst.nodes[node1] = new_group
            mst.nodes[node2] = new_group
            mst.groups[new_group] = [node1, node2]
        
        # node1 is in the tree, node2 is not -> add node2 to node1's group
        elif (mst.nodes[node1] != None) and (mst.nodes[node2] == None):
            mst.edges.append((node1, node2))

            group = mst.nodes[node1]
            mst.nodes[node2] = group
            mst.groups[group].append(node2)
        
        # node2 is in the tree, node1 is not -> add node1 to node2's group
        elif (mst.nodes[node1] == None) and (mst.nodes[node2] != None):
            mst.edges.append((node1, node2))

            group = mst.nodes[node2]
            mst.nodes[node1] = group
            mst.groups[group].append(node1)

        # both nodes are in the tree in different groups -> merge groups
        elif (mst.nodes[node1] != None) and (mst.nodes[node2] != None) and (mst.nodes[node1] != mst.nodes[node2]):
            mst.edges.append((node1, node2))

            group1 = mst.nodes[node1]
            group2 = mst.nodes[node2]
            for node in mst.groups[group2]:
                mst.nodes[node] = group1
            mst.groups[group1] += mst.groups[group2]
            del mst.groups[group2]

        else:
            raise Exception('Error in minimum spanning tree algorithm.')
        
    distance_matrix['mst'] = distance_matrix.apply(lambda row: (row.hadm1, row.hadm2) in mst.edges, axis=1)

    return mst.edges, distance_matrix

if __name__ == "__main__":
    import pandas as pd
    distance1 = pd.read_csv('./test_distance_matrix1.csv')
    distance2 = pd.read_csv('./test_distance_matrix2.csv')

    tree1, _ = make_minimum_spanning_tree(distance1)
    tree2, _ = make_minimum_spanning_tree(distance2)

    print(f"Test 1 passed: {tree1 == [('A', 'B'), ('C', 'D'), ('A', 'C'), ('A', 'E')]}") # made up example
    print(f"Test 2 passed: {tree2 == [(7, 6), (8, 2), (6, 5), (0, 1), (2, 5), (2, 3), (0, 7), (3, 4)]}") # example from https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/#
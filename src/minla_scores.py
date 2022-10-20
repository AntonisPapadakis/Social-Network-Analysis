import os
import numpy as np
import pandas as pd
import networkx as nx
import directories as dir
from minla_functions import LA
import warnings

def main():
    warnings.filterwarnings('ignore')
    
    random_scores = []
    simulated_annealing_scores = []
    full_search_scores = []
    fname = os.path.join(dir.data_dir, "dataset.csv")
    df = pd.read_csv(fname, delimiter=';')
    df['Snapshots'] = df['Snapshots'].str.split('-')
    
    for snapshot in range(19, 49):
        
        subgraph = []

        for index in range(len(df)):
            snapshot_range = list(map(int, df.iloc[index]['Snapshots']))
            if snapshot in range(snapshot_range[0], snapshot_range[1] + 1):
                subgraph.append(str(df.iloc[index]['id']))

        fname = os.path.join(dir.graphs_dir, f"edge_lists/{snapshot}.edges")
        g = nx.read_weighted_edgelist(fname, delimiter=",")
        G = g.subgraph(subgraph)

        nodes = sorted(G.nodes)
        adj = nx.adjacency_matrix(G, nodelist=nodes, weight='weight').A
        mapping = {n: idx for idx, n in enumerate(nodes)}
        layout = np.arange(0, len(nodes), dtype=np.int32)
        
        random_scores.append(round(LA(adj, layout), 2))
        
        fname = os.path.join(dir.simulated_layouts_dir, f"{snapshot}.txt")
        with open(fname) as f:
            layout = [mapping[line.rstrip()] for line in f]

        simulated_annealing_scores.append(round(LA(adj, layout), 2))
        
        fname = os.path.join(dir.layouts_dir, f"{snapshot}.txt")
        with open(fname) as f:
            layout = [mapping[line.rstrip()] for line in f]

        full_search_scores.append(round(LA(adj, layout), 2))
    
    df = pd.DataFrame(zip(range(19, 49), random_scores, simulated_annealing_scores, full_search_scores),
                              columns=['Snapshot', 'Random', 'Simulated Annealing Score', 'Full Search Score'])
    
    fname = os.path.join(dir.tables_dir, "minla_scores.csv")
    df.to_csv(fname)

if __name__ == "__main__":
    main()
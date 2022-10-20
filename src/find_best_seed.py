import os
import numpy as np
import pandas as pd
import networkx as nx
import directories as d
from minla_functions import simulated_annealing
import warnings


# Find the seed that returns the lowest minla score using Simulated Annealing


def main():
    warnings.filterwarnings('ignore')
    
    fname = os.path.join(d.data_dir, "dataset.csv")
    df = pd.read_csv(fname, delimiter=';')
    df['Snapshots'] = df['Snapshots'].str.split('-')

    for snapshot in range(19, 49):
        G = create_subgraph(snapshot, df)
        
        nodes = sorted(G.nodes())
        adj = nx.adjacency_matrix(G, nodelist=nodes, weight='weight').A
        layout = np.arange(0, len(nodes), dtype=np.int32)
        
        best_seed, best_score = best_sim_anneal_seed(adj, layout)
        
        fname = os.path.join(d.data_dir, "simulated_annealing_best_seeds2.txt")
        with open(fname, mode='a') as f:
            f.write(f'{snapshot}: {best_seed}\n')
        

def create_subgraph(snapshot, df):
    subgraph = []
    
    for index in range(len(df)):
        snapshot_range = list(map(int, df.iloc[index]['Snapshots']))
        if snapshot in range(snapshot_range[0], snapshot_range[1] + 1):
            subgraph.append(str(df.iloc[index]['id']))

    fname = os.path.join(d.graphs_dir, f"edge_lists/{snapshot}.edges")
    G = nx.read_weighted_edgelist(fname, delimiter=",")
    return G.subgraph(subgraph)


def best_sim_anneal_seed(adj, l):
    best_score = 550000
    for s in range(11):
        layout = l
        layout, cost = simulated_annealing(adj, layout, mit=500, seed=s)
        if cost < best_score:
            best_score = cost
            best_seed = s
    return best_seed, best_score


if __name__ == "__main__":
    main()
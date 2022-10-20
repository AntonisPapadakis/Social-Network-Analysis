import os
import numpy as np
import pandas as pd
import networkx as nx
import directories as d
from minla_functions import simulated_annealing, LA, full_search
import warnings


def main():
    warnings.filterwarnings('ignore')
    
    fname = os.path.join(d.data_dir, "dataset.csv")
    df = pd.read_csv(fname, delimiter=';')
    df['Snapshots'] = df['Snapshots'].str.split('-')

    best_seeds = {}
    with open(os.path.join(d.data_dir, "simulated_annealing_best_seeds.txt")) as f:
        for line in f:
            k, v = line.split(': ')
            best_seeds[int(k)] = int(v.strip('\n'))

    for snapshot in range (19, 49):

        subgraph = []
        seed = best_seeds[snapshot]

        print('SNAPSHOT ', snapshot)

        for index in range(len(df)):
            snapshot_range = list(map(int, df.iloc[index]['Snapshots']))
            if snapshot in range(snapshot_range[0], snapshot_range[1] + 1):
                subgraph.append(str(df.iloc[index]['id']))

        fname = os.path.join(d.graphs_dir, f"edge_lists/{snapshot}.edges")
        g = nx.read_weighted_edgelist(fname, delimiter=",")
        G = g.subgraph(subgraph)


        nodes = sorted(G.nodes)
        adj = nx.adjacency_matrix(G, nodelist=nodes, weight='weight').A
        mapping = {idx: n for idx, n in enumerate(nodes)}
        layout = np.arange(0, len(nodes), dtype=np.int32)

        print('Start: ', LA(adj, layout))
        layout, cost = simulated_annealing(adj, layout, seed=seed)
        print('Simulated Annealing: ', cost)

        layout_labels = [mapping[n] for n in layout]
        np.savetxt(os.path.join(d.simulated_layouts_dir, f"{snapshot}.txt"),
                    layout_labels, fmt="%s")
        

        layout, cost, cnt = full_search(adj, layout)
        print("Full search:", cost)
        layout_labels = [mapping[n] for n in layout]
        np.savetxt(os.path.join(d.layouts_dir, f"{snapshot}.txt"),
                layout_labels, fmt="%s")

if __name__ == "__main__":
    main()
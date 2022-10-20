
import os
import directories as dir
import networkx as nx
from networkx.algorithms import bipartite
import pandas as pd


def create_subgraph(snapshot, df):
    subgraph = []
    
    for index in range(len(df)):
        snapshot_range = list(map(int, df.iloc[index]['Snapshots']))
        if snapshot in range(snapshot_range[0], snapshot_range[1] + 1):
            subgraph.append(str(df.iloc[index]['id']))

    fname = os.path.join(dir.graphs_dir, f"edge_lists/{snapshot}.edges")
    G = nx.read_weighted_edgelist(fname, delimiter=",")
    return G.subgraph(subgraph)


def main():
    #  Bipartite Graph Details

    fname = os.path.join(dir.graphs_dir, "bipartite_graph.edges")
    G = nx.read_edgelist(fname, delimiter=',', nodetype=str)
    followers, nois = bipartite.sets(G)


    bipartite_graph_details = dict()
    bipartite_graph_details['Number of Nodes'] = len(G.nodes)
    bipartite_graph_details['Number of Edges'] = len(G.edges)
    bipartite_graph_details['Number of Politicians'] = len(nois)
    bipartite_graph_details['Number of Followers'] = len(followers)

    fname = os.path.join(dir.tables_dir, "bipartite_graph_details.csv")
    with open(fname, 'w') as f:
        for k, v in bipartite_graph_details.items():
            # f.write("%s, %s\n" % (k, v))
            f.write(f"{k}, {v}\n")


    path = os.path.join(dir.data_dir, "politicians2021/")

    politician_party = {}

    for file in os.listdir(path):
        with open(path + file, mode='r') as f:
            if not file.startswith('.'):
                for politician in f.read().splitlines():
                    politician_party[politician] = file.strip('.txt')


    fname = os.path.join(dir.graphs_dir, "bipartite_graph.edges")
    df = pd.read_csv(fname, header=None, names=['follower_id', 'politician'])

    for i in range(len(df)):
        df.loc[i, 'party'] = politician_party[df.iloc[i]['politician']]


    follower_count = dict()
    for pol in df.party.unique():
        follower_count[pol] = len(df[df['party']==pol])

    fname = os.path.join(dir.tables_dir, "parties_number_of_followers.csv")
    with open(fname, 'w') as f:
        for k, v in follower_count.items():
            f.write(f"{k}, {v}\n")


    #  Projected Graph Details

    fname = os.path.join(dir.graphs_dir, "projected_graph.edges")
    G = nx.read_weighted_edgelist(fname, delimiter=',', nodetype=str)


    projected_graph_details = dict()
    projected_graph_details['Number of Nodes'] = len(G.nodes)
    projected_graph_details['Number of Edges'] = len(G.edges)


    fname = os.path.join(dir.tables_dir, "projected_graph_details.csv")
    with open(fname, 'w') as f:
        for k, v in projected_graph_details.items():
            f.write(f"{k}, {v}\n")


    #  Number of policticians in every snapshot

    fname = os.path.join(dir.data_dir, "dataset.csv")
    df = pd.read_csv(fname, delimiter=';')
    df['Snapshots'] = df['Snapshots'].str.split('-')

    snapshot_nodes = dict()
    for snapshot in range(19, 49):
        G = create_subgraph(snapshot, df)
        snapshot_nodes[snapshot] = len(G.nodes)


    fname = os.path.join(dir.tables_dir, "snapshots_number_of_nodes.csv")
    with open(fname, 'w') as f:
        for k, v in snapshot_nodes.items():
            f.write(f"{k}, {v}\n")


if __name__ == "__main__":
    main()
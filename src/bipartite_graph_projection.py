import os
import networkx as nx
import directories as dir
from networkx.algorithms.bipartite import projection
from networkx.algorithms import bipartite


def main():
    fname = os.path.join(dir.graphs_dir, "bipartite_graph.edges")
    bipartite_g = nx.read_edgelist(fname, delimiter=",", nodetype=str)
    if nx.is_bipartite(bipartite_g):
        followers, nois = bipartite.sets(bipartite_g)
    
    G = projection.overlap_weighted_projected_graph(bipartite_g, nodes=nois, jaccard=False)
    fname = os.path.join(dir.graphs_dir, "projected_graph.edges")
    nx.write_edgelist(G, fname, delimiter=',', data=['weight'])


if __name__ == "__main__":
    main()
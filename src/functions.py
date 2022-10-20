import matplotlib.pyplot as plt
import networkx as nx


def labels_to_clusters(labels):
    """ Convert list of labels to clusters """
    num_of_nodes = len(labels)
    num_of_clusters = len(set(labels))

    clusters = []

    for i in range(num_of_clusters):
        clusters.append(list())

    for i in range(num_of_nodes):
        cluster_id = labels[i]
        clusters[cluster_id].append(i)

    return clusters


def draw_graph(g, labels, color_map, fname, weight='weight'):
    plt.figure(figsize=(12, 12))
    edges, weights = zip(*nx.get_edge_attributes(g, weight).items())
    pos = nx.spring_layout(g)
    nx.draw(g, pos, edgelist=edges, edge_color='w', width=1, edge_cmap=plt.cm.BuPu,
            node_size=250, labels=labels, node_color=color_map, font_color='w')
    plt.savefig(fname, bbox_inches='tight', pad_inches=0)
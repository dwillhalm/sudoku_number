import networkx as nx
import matplotlib.pyplot as plt
from generate_asymp_3_reg_graph import create_random_3_reg_graph

def decycling_algorithm_3_reg_graph(G: nx.Graph) -> nx.Graph:
    # Create an empty graph
    H = nx.Graph()

    for vertex in G.nodes():
        H.add_node(vertex)
        if list(G[vertex])[0] in H.nodes():
            H.add_edge(vertex, list(G[vertex])[0])
        if list(G[vertex])[1] in H.nodes():
            H.add_edge(vertex, list(G[vertex])[1])
        if list(G[vertex])[2] < vertex:
            H.add_edge(vertex, list(G[vertex])[2])
            try:
                cycle = nx.find_cycle(H, source=vertex)
                #if vertex == 48:
                #    return H
                H.remove_node(vertex)
            except nx.exception.NetworkXNoCycle:
                continue
    return H


if __name__ == "__main__":
    n = 52
    G = create_random_3_reg_graph(n)
    print(G)
    
    nx.draw(G, with_labels=True)
    plt.show()

    H = decycling_algorithm_3_reg_graph(G)
    print(H)

    nx.draw(H, with_labels=True)
    plt.show()
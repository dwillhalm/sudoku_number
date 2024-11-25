import networkx as nx
import random
import matplotlib.pyplot as plt

def create_random_3_reg_graph(n) -> nx.Graph:
    if n % 2 != 0:
        raise ValueError("n must be even")

    # Create a Hamiltonian cycle
    hamiltonian_cycle = nx.cycle_graph(n)
    G = hamiltonian_cycle.copy()

    # Create a list of unmatched nodes
    unmatched_nodes = list(range(n))

    # Randomly match the nodes
    while len(unmatched_nodes) > 1:
        node1 = random.choice(unmatched_nodes)
        node2 = node1
        while node2 == node1:
            node2 = random.choice(unmatched_nodes)
        
        # Check if there is already an edge between node1 and node2
        if not G.has_edge(node1, node2):
            G.add_edge(node1, node2)
            unmatched_nodes.remove(node1)
            unmatched_nodes.remove(node2)

        if len(unmatched_nodes) == 2 and G.has_edge(unmatched_nodes[0], unmatched_nodes[1]):
            G = hamiltonian_cycle.copy()
            unmatched_nodes = list(range(n))
    return G

if __name__ == "__main__":
    n = 52
    G = create_random_3_reg_graph(n)
    print(G)

    nx.draw(G, with_labels=True)
    plt.show()
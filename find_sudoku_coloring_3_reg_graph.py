import itertools
from tqdm import tqdm

# Helper function to limit the number of color configurations that we need to check. Used for eliminating configurations that are equivalent up to permutation of the color classes.
def f(config,color):
    try:
        index = config.index(color)
    except ValueError:
        index = -1
    return index

def generate_iterations_for_loop(onlyBalanced: bool, colors: list, numNodes: int, balancedThreshold=3):
    iter = []
    color_configurations = itertools.product(colors, repeat=numNodes)
    for config in tqdm(color_configurations, total = len(colors)**numNodes):
        if onlyBalanced:
            if f(config,0) <= f(config,1) <= f(config,2) and abs(config.count(0)-numNodes/len(colors)) <= balancedThreshold and abs(config.count(0)-numNodes/len(colors)) <= balancedThreshold and abs(config.count(0)-numNodes/len(colors)) <= balancedThreshold:
                iter.append(config)
        else:
            if f(config,0) <= f(config,1) <= f(config,2) and 0 in config and 1 in config and 2 in config:
                iter.append(config)
    return iter

# G is the original graph, H is the decycled graph
def find_coloring_3_reg_graph(G,H,onlyBalanced=True):
    colors = [0, 1, 2]
    nodes = [node for node in G.nodes() if node not in H.nodes()]

    iter = generate_iterations_for_loop(onlyBalanced, colors, len(nodes))

    best_coloring_uncolored = float('inf')

    for config in tqdm(iter):
        color_assignment = dict(zip(nodes, config))
        #print(color_assignment)
        helper = color_assignment.copy()
        uncolored_nodes = list(H.nodes())
        nodeFound = True
        colorError = False
        while len(uncolored_nodes) > 0 and nodeFound and not colorError:
            nodeFound = False
            for node in uncolored_nodes:
                adjacent_colors = {color_assignment[neighbor] for neighbor in G[node] if neighbor in color_assignment}
                #print(node, list(adjacent_colors))
                if len(adjacent_colors) == 2:
                    #print(node, list(adjacent_colors))
                    color_assignment[node] = 3 - sum(adjacent_colors)
                    nodeFound = True
                    uncolored_nodes.remove(node)
                    break
                if len(adjacent_colors) == 3:
                    colorError = True
                    break
        if len(uncolored_nodes) < best_coloring_uncolored and not colorError:
            best_coloring_uncolored = len(uncolored_nodes)
            best_coloring = color_assignment
            best_sudoku_coloring = helper
        if len(uncolored_nodes) == 0:
            return best_coloring, best_sudoku_coloring, 0
    return best_coloring, best_sudoku_coloring, best_coloring_uncolored

if __name__ == "__main__":
    iter = generate_iterations_for_loop(True, [0, 1, 2], 16)
    print(len(iter))
    iter = generate_iterations_for_loop(False, [0, 1, 2], 16)
    print(len(iter))
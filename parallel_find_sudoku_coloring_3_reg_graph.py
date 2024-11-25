from itertools import islice, product
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
import os
from multiprocessing import Manager, Process


# Helper function to limit the number of color configurations that we need to check. Used for eliminating configurations that are equivalent up to permutation of the color classes.
def f(config,color):
    try:
        index = config.index(color)
    except ValueError:
        index = -1
    return index


def generate_iterations_for_loop(onlyBalanced: bool, colors: list, numNodes: int, balancedThreshold=3):
    iter = []
    color_configurations = product(colors, repeat=numNodes)
    print("Generating efficient set of color configurations")
    for config in tqdm(color_configurations, total = len(colors)**numNodes):
        if onlyBalanced:
            if f(config,0) <= f(config,1) <= f(config,2) and abs(config.count(0)-numNodes/len(colors)) <= balancedThreshold and abs(config.count(0)-numNodes/len(colors)) <= balancedThreshold and abs(config.count(0)-numNodes/len(colors)) <= balancedThreshold:
                iter.append(config)
        else:
            if f(config,0) <= f(config,1) <= f(config,2) and 0 in config and 1 in config and 2 in config:
                iter.append(config)
    return iter


# G is the original graph, H is the decycled graph
def sudoku_coloring_worker(config_batch, nodes, G, H, progress_queue, update_frequency=1000):
    best_coloring_uncolored = float('inf')
    best_coloring = None
    best_sudoku_coloring = None
    local_progress = 0  # Tracks progress within this worker

    for config in config_batch:
        color_assignment = dict(zip(nodes, config))
        helper = color_assignment.copy()
        uncolored_nodes = list(H.nodes())
        nodeFound = True
        colorError = False

        while len(uncolored_nodes) > 0 and nodeFound and not colorError:
            nodeFound = False
            for node in uncolored_nodes:
                adjacent_colors = {color_assignment[neighbor] for neighbor in G[node] if neighbor in color_assignment}
                if len(adjacent_colors) == 2:
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

        # Increment local progress
        local_progress += 1

        # Report progress to the listener in batches
        if local_progress % update_frequency == 0:
            progress_queue.put(update_frequency)
            local_progress = 0

        if len(uncolored_nodes) == 0:
            # Report any remaining progress
            if local_progress > 0:
                progress_queue.put(local_progress)
            break

    if local_progress > 0:
        progress_queue.put(local_progress)

    return best_coloring, best_sudoku_coloring, best_coloring_uncolored


def progress_listener(progress_queue, total):
    with tqdm(total=total) as pbar:
        for update in iter(progress_queue.get, None):  # Get items until a sentinel (`None`) is received
            pbar.update(update)

def parallel_sudoku_coloring(G, H, num_workers=None, onlyBalanced=True):
    colors = [0, 1, 2]
    nodes = [node for node in G.nodes() if node not in H.nodes()]

    iter = generate_iterations_for_loop(onlyBalanced, colors, len(nodes))

    if num_workers is None:
        print("Number of workers not specified. Using all " + str(os.cpu_count()) + " available CPU cores.")
        num_workers = os.cpu_count()

    batch_size = -(-len(iter) // num_workers)  # Ceiling division
    config_batches = [list(islice(iter, batch_size)) for _ in range(num_workers)]
    #config_batches = [iter[i:i + batch_size] for i in range(0, len(iter), batch_size)]

    best_coloring_uncolored = float('inf')
    best_coloring = None
    best_sudoku_coloring = None

    manager = Manager()
    progress_queue = manager.Queue()

    print("Starting parallelized computing of (closest) Sudoku coloring")
    # Start the progress listener
    total_tasks = len(iter)
    listener = Process(target=progress_listener, args=(progress_queue, total_tasks))
    listener.start()

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(sudoku_coloring_worker, batch, nodes, G, H, progress_queue) for batch in config_batches]
        for future in as_completed(futures):
            result_coloring, result_sudoku_coloring, result_uncolored = future.result()
            if result_uncolored < best_coloring_uncolored:
                best_coloring_uncolored = result_uncolored
                best_coloring = result_coloring
                best_sudoku_coloring = result_sudoku_coloring
            if best_coloring_uncolored == 0:
                break

    # Stop the progress listener
    progress_queue.put(None)
    listener.join()

    return best_coloring, best_sudoku_coloring, best_coloring_uncolored


if __name__ == "__main__":
    iter = generate_iterations_for_loop(True, [0, 1, 2], 16)
    print(len(iter))
    iter = generate_iterations_for_loop(False, [0, 1, 2], 16)
    print(len(iter))
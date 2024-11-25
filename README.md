# Sudoku Number Calculation for 3-Regular Graphs

## Project Description
This project attempts to compute the **Sudoku number** (also known as the defining number) of random 3-regular graphs. Specifically, it generates graphs that are Hamiltonian cycles with a perfect matching and applies a decycling algorithm to it.
The set of nodes not in the decycling set is assumed to be a good candidate for a sudoku set. We try to find a coloring of those nodes that infer a maximum number of nodes. This will not always give the sudoku set but usually can be extended to one by adding a single additional node to it.

The sudoku number refers to the minimum number of nodes of a graph that need to be colored such that there is a unique extension to a $k$-coloring of the whole graph, where $k$ is the graph's chromatic number. Such a minimal set of nodes is called sudoku set (or defining set).

---

## Features
1. **Random 3-Regular Graph Generation**:
   - Generates 3-regular graphs with a Hamiltonian cycle and a perfect matching.
   - Asymptotically a random 3-regular graph is a Hamilton cycle and a perfect matching

2. **Decycling Algorithm**:
   - Returns the largest decycled graph (a tree).
   - Based on the algorithm described in:
     > **Bau, Sheng, Wormald, Nicholas C., and Zhou, Sanming.**  
     > *Decycling numbers of random regular graphs.*  
     > Random Structures & Algorithms, 21(3-4), 397–413 (2002).  
     > [DOI: 10.1002/rsa.10069](https://doi.org/10.1002/rsa.10069)  
     > [Full Article (PDF)](https://onlinelibrary.wiley.com/doi/pdf/10.1002/rsa.10069)

3. **Find Sudoku Number**:
   - Compute efficient iterator.
   - Brute force loop over iterator.

4. **Parallelized find Sudoku Number**:
   - Parallelized version to increase performance

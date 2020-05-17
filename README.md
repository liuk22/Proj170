# CS 170 Efficient Algorithms and Intractable Problems Project Spring 2020
_Contributors: Cindy Zhang, Kaichen Liu, Olivia Qin_
### Project Objective

Formally, let _G = (V, E)_ be a positive weighted, connected, undirected graph. We would like to find a tree subgraph _T_ of _G_ such that every vertex in _V_ is either adjacent to _T_ or in _T_, and the average pairwise distance of vertices in _T_ is minimized.

### Approximation Solution

We first generated a minimum spanning tree and an approximate minimum dominating set and using a steiner tree to connect the vertices in the set. These approaches would approximately minimize pairwise distance, since the MST minimizes total edge weights and the dominating set approach minimizes the number of nodes necessary to include in the network. In both solutions, after generating the tree, we pruned leaf nodes to improve the average pairwise distance while maintaining a valid network. We chose to take the minimum of the two solutions to guarantee we started out with the minimum possible average pairwise distance between the two.

From there we further optimized the solution by performing 1000 iterations of simulated annealing. We first used a heuristic to pick an edge adjacent to the tree to add to our network, which would be pruned again. We chose the edge with the highest heuristic. Considering the edge ```e = (u, v)``` where ```u``` is in the network and ```v``` is not, the heuristic was ```average_edge_weight * degree(v) - weight(e)```. We found that including nodes with a high degree had a higher probability of minimizing the average pairwise distance, since a single cell tower can service more cities. We also didn’t want to add really heavy edges, since that has more potential to increase the cost of the network.

If the pruned network after adding edge ```e``` reduced the average pairwise distance, we kept that version of the graph, otherwise we kept it with probability ```0.2```. Simulated annealing was also used in the process of pruning, where we pruned an edge if it decreased our average pairwise distance, otherwise we pruned with probability ```0.1```. Simulated annealing would help us escape local minimums and consider more options in the solution space, so we made sure that we would still consider removing the edge despite possibly temporarily increasing the average pairwise distance.

### Running the Solution
Using Python 3, install the requirements with the supplied file and running ```python3 solver.py``` will run the approximation algorithm on input graphs and output them to the output folder.

All input graphs are under the ```inputs``` folder. Graphs are formatted as ```.in``` text files as follows:
   - The first line should be the number of vertices in the input graph as an integer.
   - Each following line is a space-separated list of 3 integers in the format of ```u v l(u, v)``` as in vertex, vertex, and the weight of the edge connecting them.

_Example Input_
```
5
0 1 0.25
1 2 0.5
2 0 0.75
2 3 1.5
3 4 0.25
```

All output graphs are outputted under the ```outputs``` folder, formatted as ```.out``` text files as follows:
  - The first line contains a space-separated list of integers corresponding to the vertices in the chosen subgraph.
  - Each following line is formatted as two space-separated integers ```u v``` corresponding to an edge of the input graph.

_Example Output_
```
2 3 4
2 3
3 4
```

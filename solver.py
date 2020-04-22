import networkx as nx
import networkx.algorithms.approximation as naa
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
import sys
import os


def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """
    sol1 = DS_solution(G)
    sol2 = MST_solution(G)
    if average_pairwise_distance(sol1) < average_pairwise_distance(sol2):
        return sol1
    return sol2

def DS_solution(G):
    Gcopy = G.copy()
    Domset = naa.min_weighted_dominating_set(Gcopy)
    if len(Domset) == 1:
        sol = nx.Graph()
        sol.add_node(Domset.pop())
        return sol
    return naa.steinertree.steiner_tree(G, list(Domset))


def MST_solution(G):
    
    def can_remove_leaf(leaf, MST, G):
        for leaf_neighbor in G.neighbors(leaf):
            # leaf_neighbor must have at least one neighbor that's in MST that is not leaf
            current_leaf_neighbor_OK = False
            for leaf_neighbor_neighbor in G.neighbors(leaf_neighbor):
                if MST.has_node(leaf_neighbor_neighbor) and leaf_neighbor_neighbor != leaf:
                    current_leaf_neighbor_OK = True
            if not current_leaf_neighbor_OK:
                return False
        return True

    MST = nx.algorithms.minimum_spanning_tree(G)
    Gcopy = G.copy()
    ct = 1
    while (ct != 0):
        ct = 0
        MST_leaves = [x for x in Gcopy.nodes() if Gcopy.degree(x) == 1]
        for leaf in MST_leaves:
            if can_remove_leaf(leaf, MST, G):
                MST.remove_node(leaf)
                Gcopy.remove_node(leaf)
                ct += 1
    return MST

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    for file in os.listdir('./inputs'):
        G = read_input_file('./inputs/' + file, 100)
        T = solve(G)
        assert is_valid_network(G, T)
        print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
        write_output_file(T, 'outputs/{0}.out'.format(file[:-3]))

import networkx as nx
import networkx.algorithms.approximation as naa
from networkx.algorithms.approximation import steinertree
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
import sys
import os
import random


def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """
    # heuristic of scalar * degree - edgeweight
    sol1 = DS_solution(G)
    sol2 = MST_solution(G)
    best_sol = None
    if average_pairwise_distance(sol1) < average_pairwise_distance(sol2):
        best_sol = sol1
    else:
        best_sol = sol2
    best_sol_copy = best_sol.copy()
    for _ in range(100):
        edge_to_add = ()
        for u in best_sol_copy.nodes():
            for v in G.neighbors(u):
                if not best_sol_copy.has_node(v):
                    e = (u, v)
                    heuristic = G.degree(u) - G[u][v]['weight']
                    if edge_to_add is ():
                        edge_to_add = (e, heuristic)
                    else:
                        edge_to_add = min([edge_to_add, (e, heuristic)], key=lambda x: -1 * x[1])
        if edge_to_add is not ():
            best_sol_copy = replace_edge(best_sol_copy, edge_to_add[0])

    if average_pairwise_distance(best_sol_copy) > average_pairwise_distance(best_sol):
        return best_sol
    return best_sol_copy


def replace_edge(sol, edge):
    prob = 0.2
    sol_copy = sol.copy()
    sol_copy.add_edge(*edge)
    sol_copy = MST_solution(G, sol_copy)
    assert is_valid_network(G, sol_copy), "after"
    apd_copy = average_pairwise_distance(sol_copy)
    apd_og = average_pairwise_distance(sol)
    if apd_copy < apd_og:
        return sol_copy
    elif random.random() > prob:
        return sol
    else:
        return sol_copy


def DS_solution(G):
    Gcopy = G.copy()
    Domset = naa.min_weighted_dominating_set(Gcopy)
    if len(Domset) == 1:
        sol = nx.Graph()
        sol.add_node(Domset.pop())
        return sol
    return steinertree.steiner_tree(G, list(Domset))


def MST_solution(G, MST=None):
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

    if not MST:
        MST = nx.algorithms.minimum_spanning_tree(G)
    Gcopy = G.copy()
    ct = 1
    while (ct != 0):
        ct = 0
        MST_leaves = [x for x in MST.nodes() if MST.degree(x) == 1]
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
#        assert False
        assert is_valid_network(G, T)
        print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
        write_output_file(T, 'outputs/{0}.out'.format(file[:-3]))

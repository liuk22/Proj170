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

    # TODO: your code here!
    Gcopy = G.copy()
    Domset = naa.min_weighted_dominating_set(Gcopy)
    if len(Domset) == 1:
        sol = nx.Graph()
        sol.add_node(Domset.pop())
        return sol
    return naa.steinertree.steiner_tree(G, list(Domset))

# Usage: python3 solver.py test.in

if __name__ == '__main__':
#    assert len(sys.argv) == 1
#    path = sys.argv[1]
#    max_size = int(sys.argv[2])
    for file in os.listdir('./inputs'):
        G = read_input_file('./inputs/' + file, 100)
        T = solve(G)
#        assert False
        assert is_valid_network(G, T)
        print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
        write_output_file(T, 'outputs1/{0}.out'.format(file[:-3]))

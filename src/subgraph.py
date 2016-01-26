import os
import sys
import networkx as nx

# Does the graph G have a subgraph G' \in G that is isomorphic to H?

# https://adriann.github.io/Ullman%20subgraph%20isomorphism.html
# http://stackoverflow.com/questions/17480142/is-there-any-simple-example-to-explain-ullmann-algorithm
# http://stackoverflow.com/questions/13537716/how-to-partially-compare-two-graphs/13537776#13537776
# http://oldwww.prip.tuwien.ac.at/teaching/ss/strupr/vogl.pdf

## Baby case:
# G =  1
#    /   \
#   2     3
#  / \   / \
# 4  5  6  7
#
# H =  8
#    /   \
#   9    10

# Create G and H
G = nx.Graph()
H = nx.Graph()

G.add_nodes_from([1,2,3,4,5,6,7])
G.add_edge(1,2)
G.add_edge(1,3)
G.add_edge(2,4)
G.add_edge(2,5)
G.add_edge(3,6)
G.add_edge(3,7)

H.add_nodes_from([8,9,10])
H.add_edge(8,9)
H.add_edge(8,10)

print nx.is_tree(G)
print nx.is_tree(H)

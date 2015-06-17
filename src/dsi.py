import os
import sys
import networkx as nx

# Algorithm
# 1. for each rooted and directed subtree in G starting at internal node G(u)
# 2. create bipartite graph with k sons of G(u) and H(w) (w is the root of H) (see paper)
# 3. if it has a perfect matching, then done.

# SEE: https://goo.gl/0TX8cJ

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

print "Is G a tree?", nx.is_tree(G)
print "Is H a tree?", nx.is_tree(H)

# Run the algorithm
r = G.nodes()[0] 

def find_leaves(G, r):
    queue = [(r, None)]
    leaves = []
    visited = []
    children = {}
    parentOf = {}
    while len(queue) > 0:
        (curr, prev) = queue.pop(0)
        if curr not in visited:
            visited.append(curr)
            if curr not in children:
                children[curr] = []
            neighbors = G.neighbors(curr)
            if len(neighbors) == 1:
                parentOf[curr] = prev
                leaves.append(curr)
            else:
                if prev != None and prev in neighbors:
                    parentOf[curr] = prev
                    neighbors.remove(prev)
                for n in neighbors:
                    queue.append((n, curr))
                    children[curr].append(n)
    return leaves, children, parentOf

def get_subtree_rooted_at(G, u, children):
    H = nx.Graph()
    H.add_node(u)
    pass # TODO: add all children recursively below to H

G_leaves, G_children, G_parentOf = find_leaves(G, G.nodes()[0])
H_leaves, H_children, H_parentOf = find_leaves(H, H.nodes()[0])

# DP memory
subtree = {}

# Run the algorithm
for l in G_leaves:
    # call up the tree
    pass





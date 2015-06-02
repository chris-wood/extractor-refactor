import os
import sys
import networkx as nx

# alg: http://www.cs.bgu.ac.il/~dekelts/publications/subtree.pdf
# input: G and H
# output: YES if G contains a subtree isomorphic to H, NO otherwise

# 1. select a vertex r of G to be the root of G
# 2. For all u \in H, v \in G, S(v, u) \gets \null
# 3. For all leaves v of G^r do
# 4.   For all leaves u of H do S(v, u) \gets N(u)
# 5. For all internal vertices v of G^r in postorder do   
# 6.   Let v1,\dots,vt be the children of v
# 7.   For all vertices u = u_0 of H with degree at most (t + 1) do
# 8.     Let u1,\dots,us be the neighbors of of u
# 9.     Construct a bipartite graph B(v, u) = (X, Y, E_{vu}), where X = {u1,\dots,us} Y = {v1,\dots,vt}, and E_{vu} = {u_i v_j : u \in S(v_j, u_i) }
# 10.    For all 0 \leq i \leq s do
# 11.      Compute the size m_i of a maximum matching between X_i and Y
# 12.    S(v, u) \gets {u_i : m_i = |X_i|, 0 \leq i \leq s}
# 13.    If u \in S(v, u) then Return YES 
# 14.   end For
# 15. end For
# 16. Return NO

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

# Run the algorithm
r = G.nodes()[0] 

def find_leaves(G, r):
	queue = [r]
	leaves = []
	visited = []
	while len(queue) > 0:
		curr = queue.pop(0)
		if curr not in visited:
			visited.append(curr)
			neighbors = G.neighbors(curr)
			if len(neighbors) == 1:
				leaves.append(curr)
			else:
				queue = queue + neighbors
	return leaves

def postorder(G, curr, nodes):
	neighbors = filter(lambda n : n in nodes, G.neighbors(curr))
	for n in neighbors:
		postorder(G, n, nodes)
	nodes.append(curr)

def find_internals(G, r, leaves):
	nodes = []
	postorder(G, r, nodes)
	return filter(lambda x : x in leaves, nodes)

# Enumerate all leaves in G by BFS
leaves = find_leaves(G, r)

# Initialize the S map
S = {}
for u in H.nodes():
	for v in G.nodes():
		S[(v,u)] = []

# Initialize S[] based on the leaves of G to start
for gl in leaves:
	for u in H.nodes():
		hleaves = find_leaves(H, u)
		for hl in hleaves:
			S[(gl, hl)] = H.neighbors(u)

# Main loop
internals = find_internals(G, r, leaves)
print internals



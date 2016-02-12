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

def pause(locals):
    while True:
        variable = raw_input("> ")
        if variable in locals:
            print locals[variable]
        elif len(variable) == 0:
            return

def find_leaves(G, r):
    queue = [(r, None)]
    leaves = []
    visited = []
    children = {}
    while len(queue) > 0:
        (curr, prev) = queue.pop(0)
        if curr not in visited:
            visited.append(curr)
            if curr not in children:
                children[curr] = []
            neighbors = G.neighbors(curr)
            if len(neighbors) == 1:
                leaves.append(curr)
            else:
                if prev != None and prev in neighbors:
                    neighbors.remove(prev)
                for n in neighbors:
                    queue.append((n, curr))
                    children[curr].append(n)
    return leaves, children

def postorder(G, parent, curr, nodes):
    neighbors = G.neighbors(curr)
    neighbors = filter(lambda n : n not in nodes, neighbors)
    if parent in neighbors:
        neighbors.remove(parent)
    for n in neighbors:
        postorder(G, curr, n, nodes)
    nodes.append(curr)

def find_internals(G, r, leaves):
    nodes = []
    postorder(G, -1, r, nodes)
    return filter(lambda x : x not in leaves, nodes)

def find_nodes_of_at_most_degree(G, t):
    matches = []
    for n in G.nodes():
        if len(G.neighbors(n)) <= t:
            matches.append(n)
    return matches

def subtree_isomorphism(G, H):
    # Run the algorithm
    r = G.nodes()[0]

    # Enumerate all leaves in G by BFS
    leaves, children = find_leaves(G, r)
    # print "Leaves:", leaves
    # print "Children:", children

    # Initialize the S map
    S = {}
    for u in H.nodes():
        for v in G.nodes():
            S[(v,u)] = set()

    # Initialize S[] based on the leaves of G to start
    for gl in leaves:
        for u in H.nodes():
            hleaves, dummyChildren = find_leaves(H, u)
            for hl in hleaves:
                S[(gl, hl)] = H.neighbors(u)

    ### CORRECT TO HERE

    # Main loop
    internals = find_internals(G, r, leaves)

    for i,v in enumerate(internals):
        childs = children[v]
        t = len(childs)
        hdegrees = find_nodes_of_at_most_degree(H, t + 1)
        for j,u in enumerate(hdegrees):
            uneighbors = H.neighbors(u) # u1,...,us
            s = len(uneighbors)


            X = uneighbors
            Y = childs

            edgeSet = []
            for uu in X:
                for vv in Y:
                    if (vv,uu) in S:
                        if u in S[(vv, uu)]:
                            edgeSet.append((uu, vv))

            # Construct the bipartite graph between the two vertex sets
            bg = nx.Graph()
            bg.add_nodes_from(X, bipartite=0)
            bg.add_nodes_from(Y, bipartite=1)
            bg.add_edges_from(edgeSet)

            #pause(locals())

            # Try to find all the maximal matchings for all i = 0..s
            mi_vector = []
            m_star = 0
            X_star = []
            for si in range(-1, s):
                # Define X_0 = X and X_i = X \ {u_i}
                X_i = X # only if i = 0 (si == -1)
                u_i = u # fixed.
                if si >= 0:
                    u_i = X[si] # X = uneighbors
                    X_i = [uu for uu in X if uu != u_i]

                testGraph = nx.Graph()
                testGraph.add_nodes_from(X_i, bipartite=0)
                testGraph.add_nodes_from(Y, bipartite=1)

                edgeSet = []
                for uu in X_i:
                    neighbors = bg.neighbors(uu)
                    for n in neighbors:
                        edgeSet.append((uu, n))
                testGraph.add_edges_from(edgeSet)

                m_i = len(nx.maximal_matching(testGraph))
                mi_vector.append((m_i, u_i, X_i)) # record the X_i, this can be skipped

                #pause(locals())

                if m_i > m_star:
                    m_star = m_i
                    X_star = X_i

            if (v,u) not in S:
                S[(v,u)] = set()
            for (m_i, u_i, X_i) in mi_vector:
                if m_i == len(X_i):
                    S[(v, u)].add(u_i)

            if u in S[(v, u)]:
                return "YES"

    return "NO"


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

print subtree_isomorphism(G, H)

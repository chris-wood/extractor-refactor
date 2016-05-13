import os
import sys
import networkx as nx

# alg: http://www.cs.bgu.ac.il/~dekelts/publications/subtree.pdf
# input: G and H
# output: YES if G contains a subtree isomorphic to H, NO otherwise

def pause(locals):
    while True:
        variable = raw_input("> ")
        if variable in locals:
            print locals[variable]
        elif len(variable) == 0:
            return

# Create G and H
G = nx.DiGraph()
H = nx.DiGraph()

G.add_nodes_from([1,2,3,4,5,6,7])
G.add_edge(1,2)
G.add_edge(1,3)
G.add_edge(2,4)
G.add_edge(2,5)
G.add_edge(3,6)
G.add_edge(3,7)

H.add_nodes_from([2,4,5])
H.add_edge(2,4)
H.add_edge(2,5)

print nx.is_tree(G)
print nx.is_tree(H)

def match(G, H, g, h):
    if g != h:
        return False

    gchilds = G.neighbors(g)
    hchilds = H.neighbors(h)

    if len(gchilds) != len(hchilds):
        return False
    else:
        index = 0
        matches = True
        for i in range(len(gchilds)):
            matches |= match(G, H, gchilds[i], hchilds[i])
        return matches


root = G.nodes()[0]
stack = [root]

root = H.nodes()[0]

while len(stack) > 0:
    curr = stack.pop()
    if curr == root and match(G, H, curr, root):
        print curr, root
        print "Good!"
        # sys.exit(1)
    for child in G.neighbors(curr):
        stack.insert(0, child)

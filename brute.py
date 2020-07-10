import itertools
import networkx as nx
import pygraphviz as pgv

nnodes = 8
ncolors = 2

indlist = [
    [1, 2, 6, 7],
    [0, 2, 3, 7],
    [0, 1, 3, 4],
    [1, 2, 4, 5],
    [2, 3, 5, 6],
    [3, 4, 6, 7],
    [4, 5, 7, 0],
    [5, 6, 0, 1]
]

color2hex = {
    0: 'blue',
    1: 'green',
    2: 'yellow'
}

def list2nx(indlist, coloring):
    G = pgv.AGraph(directed=False)
    G.node_attr['style'] = 'filled'
    for node, color in enumerate(coloring):
        G.add_node(node, fillcolor=color2hex[color])
    for node, indnodes in enumerate(indlist):
        for indnode in sorted(indnodes):
            G.add_edge(node, indnode)
    return G

def printmatrix(m):
    for l in m:
        if l != None:
            print(l)
        else:
            print(list([0 for _ in range(ncolors)]))

assert(len(indlist) == nnodes)

colors = list([ c for c in range(ncolors) ])

ans = []

for i, nodes_comb in enumerate(itertools.product(colors, repeat=nnodes)):
    color_state = list([ None for _ in range(ncolors) ])
    for node in range(nnodes):
        state = list([ 0 for _ in range(ncolors) ])
        for indnode in indlist[node]:
            state[ nodes_comb[indnode] ] += 1
        if color_state[ nodes_comb[node] ] != None and state != color_state[ nodes_comb[node] ]:
            break
        color_state[ nodes_comb[node] ] = state
    else:
        print(len(ans) + 1)
        printmatrix(color_state)
        ans.append(nodes_comb)

for i, coloring in enumerate(ans):
    G = list2nx(indlist, coloring)
    G.draw('{}.png'.format(i+1), prog='circo')

print(len(ans), ncolors ** nnodes)
# for c in ans:
#     print(c)
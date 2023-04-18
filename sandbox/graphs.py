#%%
import igraph as ig
import uuid

g1 = ig.Graph(n=3, edges=[(1,2)])
g2 = ig.Graph(n=3, edges=[(0,1)])
g1.vs[:]['name'] = ['a', 'b', 'c']
g2.vs[:]['name'] = ['d', 'e', 'f']
print(g1)
print(g2)

# %%
g2.connected_components(mode='weak')[0]
# %%
# figure out subgraphs
sg = g2.subgraph(g2.vs.select(name_in=['d', 'e']))
print(sg)
# %%
g3 = g1 + sg
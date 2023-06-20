#%%
import igraph as ig

g = ig.Graph(directed=True)
g.add_vertices(3)
g.add_edges([(0, 1), (2, 0)])

for c in g.connected_components(mode="weak"):
    pass

#%%
g.bfs(0, mode="out")
# %%
ig.plot(g)

# %%

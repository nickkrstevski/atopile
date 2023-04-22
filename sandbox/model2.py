#%%
import igraph as ig

# we've got 4 types of verticies
# 1. block
# 2. package
# 3. pin

# 4. ethereal_pin

# we're going to have 2 types of edges
# 1. connects_to
# 2. part_of

# we expect an attribute "type" to exist on all verticies and edges, and they must be one of the above spcified types
# we additionally expect an attribute "electrical_type" to exist on all ethereal_pin verticies
#%%
def plot(g: ig.Graph):
    color_dict = {
        "block": "red",
        "package": "green",
        "pin": "cyan",
        "ethereal_pin": "magenta",
        "connects_to": "blue",
        "part_of": "black",
    }
    visual_style = {}
    visual_style["vertex_color"] = [color_dict[type_name] for type_name in g.vs["type"]]
    visual_style["vertex_label"] = g.vs["ref"]
    visual_style["edge_color"] = [color_dict[type_name] for type_name in g.es["type"]]
    return ig.plot(g, **visual_style)

# eg.;

resistor = ig.Graph(directed=True)
resistor.add_vertices(
    6,
    {'type': ['ethereal_pin'] * 2 + ['pin'] * 2 + ['package'] + ['block'],
     'ref': ['1', '2', '1', '2', 'package', 'resistor'],}
)
resistor.add_edges([(0, 5), (1, 5), (2, 4), (3, 4), (4, 5)], {'type': ['part_of'] * 5})
resistor.add_edges([(0, 2), (1, 3)], {'type': ['connects_to'] * 2})

plot(resistor)

# %%
g = ig.Graph(directed=True)
g += resistor
g += resistor
plot(g)

# %%
plot(g.subgraph(g.vs.select(type_in=['pin', 'ethereal_pin'])))

# %%
resistor.vs['ref']
# %%
g.vs['ref']

# %%

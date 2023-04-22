#%%
import igraph as ig
import numpy as np
from typing import Optional

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
    visual_style["vertex_color"] = [color_dict.get(type_name, "grey") for type_name in g.vs["type"]]
    visual_style["vertex_label"] = g.vs["ref"]
    visual_style["edge_color"] = [color_dict[type_name] for type_name in g.es["type"]]
    return ig.plot(g, **visual_style)

#%%
# eg.;

resistor = ig.Graph(directed=True)
resistor.add_vertices(
    6,
    {'type': ['ethereal_pin'] * 2 + ['pin'] * 2 + ['package'] + ['block'],
     'ref': ['1', '2', '1', '2', 'package', 'resistor'],}
)
resistor.add_edges([(0, 5), (1, 5), (2, 4), (3, 4), (4, 5)], {'type': ['part_of'] * 5})
resistor.add_edges([(0, 2), (1, 3)], {'type': ['connects_to'] * 2})

# plot(resistor)

#%%
def find_vertex_at_path(g: ig.Graph, path: str):
    path_parts = path.split('.')
    candidates = g.vs.select(ref_eq=path_parts.pop(0))
    if len(candidates) > 1:
        raise ValueError(f"Multiple verticies found at path {path_parts}. Graph is invalid")
    for ref in path_parts:
        candidates = ig.VertexSeq(g, {i.index for c in candidates for i in c.neighbors(mode='in')})
        candidates = candidates.find(ref_eq=ref)
    return candidates[0]

def find_root_vertex(g: ig.Graph):
    candidates = g.vs.select(type_eq='block', _outdegree_eq=0)
    if len(candidates) > 1:
        raise ValueError("Multiple root verticies found. Graph is invalid")
    return candidates[0]

def add_block(g: ig.Graph, block: ig.Graph, block_ref: str, parent: Optional[str] = None):
    block_start_index = len(g.vs)
    block_root_index = find_root_vertex(block).index + block_start_index
    g += block
    g.vs[block_root_index]['ref'] = block_ref

    if parent:
        g.add_edge(block_root_index, find_vertex_at_path(g, parent).index, type='part_of')
    return g

#%%
g = ig.Graph(directed=True)
g.add_vertex(ref='root', type='block')
g = add_block(g, resistor, 'r1', 'root')
g = add_block(g, resistor, 'r2', 'root')
# g.add_edges([(1, 7), (2, 8), (13, 19), (14, 20)], {'type': ['connects_to'] * 2})
plot(g)

# %%

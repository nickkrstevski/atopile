import igraph as ig
from typing import Optional

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

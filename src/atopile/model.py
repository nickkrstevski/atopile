import igraph as ig
from typing import Optional

def plot(g: ig.Graph, *args, **kwargs):
    color_dict = {
        "block": "red",
        "package": "green",
        "pin": "cyan",
        "ethereal_pin": "magenta",
        "connects_to": "blue",
        "part_of": "black",
    }
    kwargs["vertex_color"] = [color_dict.get(type_name, "grey") for type_name in g.vs["type"]]
    kwargs["vertex_label"] = g.vs["ref"]
    kwargs["edge_color"] = [color_dict[type_name] for type_name in g.es["type"]]
    return ig.plot(g, *args, **kwargs)

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

def ancestory_dot_com(g: ig.Graph, v: int):
    """
    Get all ancestors of a node
    """
    connectedness = g.subgraph_edges(g.es.select(type_eq='part_of'), delete_vertices=False)
    return connectedness.dfs(v, mode='out')[0]

def whos_your_daddy(g: ig.Graph, v: int):
    """
    Get logical parent of a node
    """
    connectedness = g.subgraph_edges(g.es.select(type_eq='part_of'), delete_vertices=False)
    parent = connectedness.vs[v].neighbors(mode='out')
    if len(parent) > 1:
        raise ValueError("Multiple logical parents found. Graph is invalid")
    return parent[0]

import igraph as ig
from typing import Optional
from atopile.model.find import find_vertex_at_path, find_root_vertex, find_root_block, whos_your_daddy
from atopile.data.starter_graph import starter_graph

def add_block(g: ig.Graph, block: ig.Graph, block_ref: str, parent: Optional[str] = None):
    block_start_index = len(g.vs)
    block_root_index = find_root_block(block).index + block_start_index
    g += block
    g.vs[block_root_index]['ref'] = block_ref

    if parent:
        g.add_edge(block_root_index, find_vertex_at_path(g, parent).index, type='part_of')
    return g

def add_graph(g: ig.Graph, added_graph: ig.Graph, root_ref: str, parent: str):
    start_index = len(g.vs)
    root_index = find_root_vertex(added_graph).index + start_index
    g += added_graph
    g.vs[root_index]['ref'] = root_ref

    g.add_edge(root_index, find_vertex_at_path(g, parent).index, type='part_of')

    return added_graph

def instantiate_from_with_ref(g: ig.Graph, path: str, ref: str):
    vertex_to_instantiate = find_vertex_at_path(g, path)
    
    subgraph_vertices = g.subcomponent(vertex_to_instantiate.index, mode="in")

    sub_g = ig.Graph(directed=True)
    completed_g = ig.Graph(directed=True)

    sub_g = g.subgraph(subgraph_vertices)
    parent = whos_your_daddy(g, vertex_to_instantiate.index)
    completed_g = add_graph(g, sub_g, ref, parent['ref']) 

    return completed_g

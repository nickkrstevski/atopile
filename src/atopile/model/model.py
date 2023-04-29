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

def add_graph(g: ig.Graph, graph_to_add: ig.Graph, graph_ref: str, parent: Optional[str] = None):
    graph_start_index = len(g.vs)
    graph_root_index = find_root_vertex(graph_to_add).index + graph_start_index
    g += graph_to_add
    g.vs[graph_root_index]['ref'] = graph_ref

    print('the vertex is', find_vertex_at_path(g, parent).index)

    if parent:
        g.add_edge(graph_root_index, find_vertex_at_path(g, parent).index, type='part_of')

    g.add_edge(graph_root_index, )

    return g

def add_vertex(g: ig.Graph, ref: str, type: str, parent: Optional[str] = None):
    start_index = len(g.vs)
    vertex_index = start_index
    
    g.add_vertex()
    g.vs[vertex_index]['ref'] = ref
    g.vs[vertex_index]['type'] = type

    if parent:
        g.add_edge(vertex_index, find_vertex_at_path(g, parent).index, type='class_of')

    return g

def instantiate(g: ig.Graph, path_to_copy: str, ref_copied: str, parent: Optional[str] = None):
    
    # Find the vertex for the class to be instantiated
    vertex_to_instantiate = find_vertex_at_path(g, path_to_copy)

    # Find all the vertices below that class
    subgraph_vertices = g.subcomponent(vertex_to_instantiate.index, mode="in")
    
    # Create two subhraphs, one for the graph below the class and the other for the completed graph
    sub_g = ig.Graph(directed=True)
    completed_g = ig.Graph(directed=True)

    # Create a 
    sub_g = g.subgraph(subgraph_vertices)

    graph_start_index = len(g.vs)
    graph_root_index = find_root_vertex(graph_to_add).index + graph_start_index
    g += graph_to_add
    g.vs[graph_root_index]['ref'] = graph_ref

    print('the vertex is', find_vertex_at_path(g, parent).index)

    if parent:
        g.add_edge(graph_root_index, find_vertex_at_path(g, parent).index, type='part_of')

    g.add_edge(graph_root_index, )

    completed_g = add_graph(g, sub_g, ref_copied, parent)
    
    return completed_g

def instantiate_from_with_ref(g: ig.Graph, path: str, ref: str):
    vertex_to_instantiate = find_vertex_at_path(g, path)
    
    subgraph_vertices = g.subcomponent(vertex_to_instantiate.index, mode="in")
    

    sub_g = ig.Graph(directed=True)
    completed_g = ig.Graph(directed=True)

    sub_g = g.subgraph(subgraph_vertices)
    parent = whos_your_daddy(g, vertex_to_instantiate.index)
    completed_g = add_graph(g, sub_g, ref, parent['ref']) 

    return completed_g

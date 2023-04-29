# %%
from atopile import model

from atopile.data.voltage_divider import voltage_divider
from atopile.data.resistor import resistor
from atopile.data.starter_graph import starter_graph

from atopile.netlist.graph_to_netlist import generate_nets_dict_from_graph
from atopile.netlist.graph_to_netlist import generate_component_list_from_graph

v_div = voltage_divider
res = resistor

res = model.add_vertex(res, 'testing', 'block')

res = model.add_vertex(res, 'test2', 'ethereal_pin', 'testing')

model.plot(res)

# %%

res = model.instantiate(res, 'testing', 'copied', 'testing')
model.plot(res)
# %%
#nets = generate_nets_dict_from_graph(v_div)

#print(nets)

# print(generate_component_list_from_graph(v_div))
# model.plot(res)

# # %%

# s_graph = starter_graph
# model.plot(s_graph)
# # %%
# result = model.instantiate_from_with_ref(s_graph, 'b.e', 'test')
# #result = model.find_vertex_at_path(s_graph, 'starter_block.starter_ethereal_pin')
# model.plot(result)
# # %%

# # %%
# import igraph

# # create the original DAG
# g = igraph.Graph(directed=True)
# g.add_vertices(
#     3,
#     {'type': ['ethereal_pin'] + ['pin'] + ['block'],
#      'ref': ['1', '2', '3']}
# )
# g.add_edges([(0, 1), (1, 2)], {'type': ['connects_to'] * 2})

# model.plot(g)
# # %%

# # choose a vertex as the starting point for the subgraph
# v = 2

# res = model.instantiate_from_with_ref(res, v, 'ref')
# # # find all vertices and edges below the starting vertex
# # subgraph_vertices = g.subcomponent(v, mode="out")
# # print(subgraph_vertices)

# # h = igraph.Graph(directed=True)
# # h = g.subgraph(subgraph_vertices)
# model.plot(res)
# # %%
# # create the subgraph
# g = model.add_block(g, h, 'test', '1') 



# # add the subgraph to the new graph
# #h = g.compose(subgraph)

# # add an edge from vertex 1 in the new graph to the first vertex of the subgraph
# #h.add_edges([(0, len(subgraph_vertices))])
# print(h)
# model.plot(g)

# %%

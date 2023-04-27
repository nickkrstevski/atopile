import igraph as ig

starter_graph = ig.Graph(directed=True)
starter_graph.add_vertices(
    4,
    {'type': ['ethereal_pin'] + ['pin'] + ['package'] + ['block'],
     'ref': ['e', 'p', 'a', 'b'],}
)
starter_graph.add_edges([(0, 3), (1, 0), (2, 3)], {'type': ['class_of'] * 3})

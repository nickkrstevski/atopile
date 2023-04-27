import igraph as ig
from atopile import model

from atopile.data.starter_graph import starter_graph

resistor = ig.Graph(directed=True)

resistor = model.add_block(resistor, starter_graph, 'block')
#resistor = model.instantiate_pin(resistor, child_graph)
# resistor.add_vertices(
#     6,
#     {'type': ['ethereal_pin'] * 2 + ['pin'] * 2 + ['package'] + ['block'],
#      'ref': ['1', '2', '1', '2', 'package', 'block'],}
# )
# resistor.add_edges([(0, 5), (1, 5), (2, 4), (3, 4), (4, 5)], {'type': ['part_of'] * 5})
# resistor.add_edges([(0, 2), (1, 3)], {'type': ['connects_to'] * 2})

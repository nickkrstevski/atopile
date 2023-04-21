from typing import Optional
from . import model
import igraph as ig
from uuid import uuid4

type_graph = ig.Graph(n=1, directed=True)
heirachy_graph = ig.Graph(n=1, directed=True)
electrical_graph = ig.Graph()

# we're gonna do this in three passes
# 1. create all the types
# 2. create all the instances
# 3. create all the connections

def make_block(name: str, type_graph: ig.Graph, heirachy_graph: ig.Graph, instance_of: Optional[model.Block] = None, derived_from: Optional[model.Block] = None, part_of: Optional[model.Block] = None):
    """"""

    if instance_of and derived_from:
        raise ValueError("Cannot be both instance_of and derived_from")

    if instance_of:
        # same exact type as it's class
        block_type = instance_of.type
    else:
        # class node in its own right
        block_type = model.GraphNode(
            graph=type_graph,
            id=str(uuid4()),
        )
        type_graph.add_vertex(block_type.id)

        if derived_from:
            # link it to it's parents type
            type_graph.add_edge(block_type.id, derived_from.type.id)

    # classes exist on the heirachy because they may have subcomponents
    # instances either should have something under them, or be under something
    # otherwise this is a wicked boring circuit...
    block_heirachy = model.GraphNode(
        graph=heirachy_graph,
        id=str(uuid4()),
    )

    # if this is being generated as a subcomponent of something, link it up
    if part_of:
        heirachy_graph.add_edge(block_heirachy.id, part_of.heirarchy_node.id)

    block = model.Block(
        name=name,
        type=block_type,
        heirachy=block_heirachy,
        ethereal_pins=[],
        package=None,
    )

    # attach objects to graph nodes
    if not instance_of:
        type_graph.vs[block_type.id]['object'] = block
    heirachy_graph.vs[block_heirachy.id]['object'] = block

    return block

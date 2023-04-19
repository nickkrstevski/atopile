from atopile.model import model
import igraph as ig
from uuid import uuid4
from typing import List

heirachy_graph = ig.Graph(directed=True)
type_graph = ig.Graph(directed=True)
electrical_graph = ig.Graph()

def make_graph_node(graph: ig.Graph):
    node = model.GraphNode(
        graph=graph,
        id=str(uuid4()),
    )
    graph.add_vertex(node.id)
    return node

root_pin_type = make_graph_node(type_graph)

# create a 0603 pacakge for resistors
def make_resistor_package():
    package = model.Package(
        name="0603",
        footprint="0603",
        pins=[
            model.Pin(
                name="1",
                pad="1",
                type=root_pin_type,
                electrical_node=make_graph_node(electrical_graph)
            ),
            model.Pin(
                name="2",
                pad="2",
                type=root_pin_type,
                electrical_node=make_graph_node(electrical_graph)
            ),
        ]
    )

    for pin in package.pins:
        electrical_graph.vs.select(name_eq=pin.electrical_node.id)['object'] = pin
        electrical_graph.vs.select(name_eq=pin.electrical_node.id)['parent'] = package

    return package

resistor_type = make_graph_node(type_graph)

# create a 0603 pacakge for resistors
def make_resistor_block(name: str):
    block = model.Block(
        name=name,
        package=make_resistor_package(),
        ethereal_pins=[
            model.EtherealPin(
                name="1",
                type=root_pin_type,
                electrical_node=make_graph_node(electrical_graph)
            ),
            model.EtherealPin(
                name="2",
                type=root_pin_type,
                electrical_node=make_graph_node(electrical_graph)
            ),
        ],
        type=resistor_type,
        blocks=[],
        hierarchy_node=make_graph_node(heirachy_graph),
    )

    for pin, ethereal_pin in zip(block.package.pins, block.ethereal_pins):
        electrical_graph.add_edge(pin.electrical_node.id, ethereal_pin.electrical_node.id)
        electrical_graph.vs.select(name_eq=pin.electrical_node.id)['object'] = pin
        electrical_graph.vs.select(name_eq=pin.electrical_node.id)['parent'] = block

    return block

resistor_class = make_resistor_block("resistor")

v_div_type = make_graph_node(type_graph)

def make_vdiv_block(name: str):
    r1 = make_resistor_block("r1")
    r2 = make_resistor_block("r2")

    block = model.Block(
        name=name,
        package=None,
        ethereal_pins=[
            model.EtherealPin(
                name="1",
                type=root_pin_type,
                electrical_node=make_graph_node(electrical_graph)
            ),
            model.EtherealPin(
                name="2",
                type=root_pin_type,
                electrical_node=make_graph_node(electrical_graph)
            ),
            model.EtherealPin(
                name="3",
                type=root_pin_type,
                electrical_node=make_graph_node(electrical_graph)
            ),
        ],
        type=v_div_type,
        blocks=[
            r1,
            r2,
        ],
        hierarchy_node=make_graph_node(heirachy_graph),
    )

    for pin in block.ethereal_pins:
        electrical_graph.vs.select(name_eq=pin.electrical_node.id)['object'] = pin
        electrical_graph.vs.select(name_eq=pin.electrical_node.id)['parent'] = block

    heirachy_graph.add_edge(block.blocks[0].hierarchy_node.id, block.hierarchy_node.id)
    electrical_graph.add_edge(r1.ethereal_pins[0].electrical_node.id, block.ethereal_pins[0].electrical_node.id)
    electrical_graph.add_edge(r1.ethereal_pins[1].electrical_node.id, r2.ethereal_pins[0].electrical_node.id)
    electrical_graph.add_edge(r1.ethereal_pins[1].electrical_node.id, block.ethereal_pins[1].electrical_node.id)
    electrical_graph.add_edge(r2.ethereal_pins[1].electrical_node.id, block.ethereal_pins[2].electrical_node.id)

    return block

v_div_class = make_vdiv_block("v_div")

v_div_1 = make_vdiv_block("v_div_1")
v_div_2 = make_vdiv_block("v_div_2")

root_block = model.Block(
    name="root",
    package=None,
    ethereal_pins=[],
    type=make_graph_node(type_graph),
    blocks=[
        v_div_1,
        v_div_2,
    ],
    hierarchy_node=make_graph_node(heirachy_graph),
)

heirachy_graph.add_edge(v_div_1.hierarchy_node.id, root_block.hierarchy_node.id)
heirachy_graph.add_edge(v_div_2.hierarchy_node.id, root_block.hierarchy_node.id)

electrical_graph.add_edge(v_div_1.ethereal_pins[0].electrical_node.id, v_div_2.ethereal_pins[0].electrical_node.id)
electrical_graph.add_edge(v_div_1.ethereal_pins[1].electrical_node.id, v_div_2.ethereal_pins[1].electrical_node.id)
electrical_graph.add_edge(v_div_1.ethereal_pins[2].electrical_node.id, v_div_2.ethereal_pins[2].electrical_node.id)

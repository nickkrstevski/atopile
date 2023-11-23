import logging
from contextlib import contextmanager
from typing import Any, Dict, List, Literal, Optional, TYPE_CHECKING, Iterable

import click
import json
import uvicorn
import hashlib
import uuid
from rich.console import Console
from rich.table import Table, Column

import attrs as attrs

from atopile.cli.common import ingest_config_hat
from atopile.model.accessors import ModelVertexView
from atopile.model.model import EdgeType, Model, VertexType
from atopile.parser.parser import build_model
from atopile.project.config import BuildConfig
from atopile.project.project import Project
from atopile.model.visitor import ModelVisitor
from atopile.targets.netlist.nets import find_nets, NetType

# configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


@attrs.define
class Cell: # called cell in the context of yosys netlists
    # mandatory external
    type: str
    port_directions: dict[str:str]
    connections: dict[str:list]
    # mandatory internal
    # source: ModelVertexView

@attrs.define
class Port:
    # mandatory external
    direction: str
    bits: list[str]
    # mandatory internal
    # source: ModelVertexView

@attrs.define
class Module:
    # mandatory external
    ports: dict[Port]
    cells: dict[Cell]

@attrs.define
class Modules:
    # mandatory external
    modules: dict[Module]

conversion_function = lambda x: x.path

class Roley():
    def __init__(self, model: Model) -> None:
        self.model = model
        self.all_verticies: List[ModelVertexView] = []
        self.block_stack: List[ModelVertexView] = []
        self.port_stack: List[ModelVertexView] = []
        self.modules: Modules|None = None
        self.nets_mvvs: List[NetType] = find_nets(self.model)
        net_paths_list = []
        for net_mvvs in self.nets_mvvs:
            net_paths = list(map(conversion_function, net_mvvs))
            net_uid = generate_net_uid(net_paths)
            net_paths_list.append((net_uid, net_paths))
        self.nets_id_and_paths: List[tuple[int,List[str]]] = net_paths_list
        #TODO: does the new compiler provide a type for nets_paths?

    def process_port(self, port: ModelVertexView, is_inverted: bool = False) -> Port:
        #TODO: kind of a mess to figure out the pin direction. See if can be improved later.
        pin_adjacents_in = list(port.get_adjacents_with_edge_types("in", EdgeType.connects_to))
        neighbor_connected_pins_in: List[ModelVertexView] = []
        for pin_adjacent in pin_adjacents_in:
            if port.parent_path != pin_adjacent[1].parent_path:
                neighbor_connected_pins_in.append(pin_adjacent[1])

        pin_adjacents_out = list(port.get_adjacents_with_edge_types("out", EdgeType.connects_to))
        neighbor_connected_pins_out: List[ModelVertexView] = []
        for pin_adjacent in pin_adjacents_out:
            if port.parent_path != pin_adjacent[1].parent_path:
                neighbor_connected_pins_out.append(pin_adjacent[1])

        if bool(is_inverted) != bool(len(neighbor_connected_pins_in) >= len(neighbor_connected_pins_out)):
            pin_direction = 'input'
        else:
            pin_direction = 'output'

        port_id = 0
        for net in self.nets_id_and_paths:
            for pin_or_signal_path in net[1]:
                if port.path == pin_or_signal_path:
                    port_id = net[0] #TODO: having a dict might make this more readable
        neighbor_connected_pins = neighbor_connected_pins_out + neighbor_connected_pins_in
        neighbor_connected_pins_paths = []
        for neighbor in neighbor_connected_pins:
            neighbor_connected_pins_paths.append(generate_uid_from_path(neighbor.path))

        return (port.ref, Port(pin_direction, [port_id])) #TODO: I actually think this was not necessary based on the netlist standard


    def process_block(self, block: ModelVertexView) -> tuple[str, Cell]:
        # get all the pins, signals and interfaces part of that block
        return_list = block.get_adjacents("in", EdgeType.part_of)
        available_list: List[ModelVertexView] = []
        for element in return_list:
            element_type = element.vertex_type
            if (element_type == VertexType.pin or element_type == VertexType.signal or element_type == VertexType.interface):
                available_list.append(element)
        # create pin and signal clusters
        port_clusters: List[tuple[int, List[ModelVertexView]]] = []
        for port_mvv in available_list:
            port_cluster: tuple[int, List[ModelVertexView]] = (0,[])
            port_cluster[0] += generate_uid_from_path(port_mvv)
            port_cluster[1].append(port_mvv)
            connected_neighbors_list = port_mvv.get_adjacents("in", EdgeType.connects_to) + port_mvv.get_adjacents("out", EdgeType.connects_to)
            for con_neighbor in connected_neighbors_list:
                if con_neighbor.parent_path == port_mvv.parent_path:
                    port_cluster[0] += generate_uid_from_path(con_neighbor)
                    port_cluster[1].append(con_neighbor)
            port_clusters.append(port_cluster)

        # process the pins, ...
        ports: List[tuple[str,Port]] = []
        for port_mvv in available_list:
            ports.append(self.process_port(port_mvv))

        output_port_dict = {}
        for port in ports:
            output_port_dict[port[0]] = port[1].direction

        output_connections = {}
        for port in ports:
            output_connections[port[0]] = port[1].bits

        return (block.ref, Cell(block.ref, output_port_dict, output_connections))


    def build_netlist(self, root_node) -> Modules:
        # need to check that the node is of type module
        root_mvv = ModelVertexView.from_path(self.model, root_node)
        return_list = root_mvv.get_adjacents("in", EdgeType.part_of)

        # list all the components and modules within the module
        for element in return_list:
            if element.vertex_type == VertexType.module or element.vertex_type == VertexType.component:
                self.block_stack.append(element)

        # list all the signals and interfaces within the module
        for element in return_list:
            if element.vertex_type == VertexType.signal or element.vertex_type == VertexType.interface:
                self.port_stack.append(element)

        # building the port dict out
        port_dict = {}
        for port in self.port_stack:
            processed_port = self.process_port(port, True)
            port_dict[processed_port[0]] = processed_port[1]

        # building the cell dict out
        cell_dict: dict[str:Cell] = {}
        for block in self.block_stack:
            cell = self.process_block(block)
            cell_dict[cell[0]] = cell[1]

        self.modules = Modules({'Vdiv':Module(port_dict,cell_dict)})

        # for list_paths in self.nets_id_and_paths:
        #     print(list_paths[0], list_paths[1])
        #     print('=========')

def generate_uid_from_path(path: str) -> str:
    path_as_bytes = path.encode('utf-8')
    hashed_path = hashlib.blake2b(path_as_bytes, digest_size=16).digest()
    return int(int(uuid.UUID(bytes=hashed_path))>>115)

def generate_net_uid(paths: List) -> int:
    # let's just take the first element in the list as the uid
    return generate_uid_from_path(paths[0])


# configure UI
@click.command()
@ingest_config_hat
@click.option("--debug/--no-debug", default=False)
def netlistsvg(
    project: Project, build_config: BuildConfig, debug: bool
):
    """
    Inspect the available pins of a component within the context of a module
    eg. `ato inspect path/to/source.ato:module.path`
    """

    if debug:
        # FIXME: Do we need this?
        import atopile.parser.parser

        atopile.parser.parser.log.setLevel(logging.DEBUG)

    # build core model
    model = build_model(project, build_config)

    # cell = Cell('r_v', {'A':'input', 'B':'output'}, {'A': [2], 'B': [2]})
    # cell_2 = Cell('r_v', {'A':'input', 'B':'output'}, {})
    # port = Port('output', [2])
    # module = Module({'vout':attrs.asdict(port)},{'r1': attrs.asdict(cell), 'r2':attrs.asdict(cell_2)})
    # module_1 = Modules({'vdiv' : module})
    on_a_roll = Roley(model)
    on_a_roll.build_netlist(build_config.root_node)
    module_1 = on_a_roll.modules


    with open("data.json", "w") as json_file:
        json.dump(attrs.asdict(module_1), json_file)



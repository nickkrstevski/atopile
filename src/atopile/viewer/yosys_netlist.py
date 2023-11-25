import logging
from contextlib import contextmanager
from typing import Any, Dict, List, Literal, Optional, TYPE_CHECKING, Iterable

import click
import json
import hashlib
import uuid

import attrs as attrs

from atopile.cli.common import ingest_config_hat
from atopile.model.accessors import ModelVertexView
from atopile.model.model import EdgeType, Model, VertexType
from atopile.parser.parser import build_model
from atopile.project.config import BuildConfig
from atopile.project.project import Project
from atopile.model.visitor import ModelVisitor
from atopile.targets.netlist.nets import find_nets, NetType

@attrs.define
class Cell: # called cell in the context of yosys netlists
    # mandatory external
    type: str
    port_directions: Dict[str:str]
    connections: Dict[str:list]
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
    ports: Dict[Port]
    cells: Dict[Cell]

@attrs.define
class Modules:
    # mandatory external
    modules: Dict[Module]

def make_list_friendly(things: Iterable[str]) -> str:
    return ", ".join(thing for thing in things)

def join_pin_signal_str(pins: str, signals: str) -> str:
    if not pins and signals:
        return signals
    elif pins and not signals:
        return pins
    return pins + ":" + signals

def generate_uid_from_path(path: str) -> str:
    path_as_bytes = path.encode('utf-8')
    hashed_path = hashlib.blake2b(path_as_bytes, digest_size=16).digest()
    # bit shifting to reduce id size
    return int(int(uuid.UUID(bytes=hashed_path))>>115)

conversion_function = lambda x: x.path


class Roley():
    """
    Helper class to build YOSYS netlists
    """
    def __init__(self, model: Model) -> None:
        self.model = model
        self.all_verticies: List[ModelVertexView] = []
        self.block_stack: List[ModelVertexView] = []
        self.port_stack: List[ModelVertexView] = []
        self.modules: Modules|None = None
        self.nets_mvvs: List[NetType] = find_nets(self.model)
        # for each net, we want a list of port paths as well as a unique identifier used for the netlist generation
        net_paths_list = []
        for net_mvvs in self.nets_mvvs:
            net_paths = list(map(conversion_function, net_mvvs))
            # we generate a uid from the first element in the list
            net_uid = generate_uid_from_path(net_paths[0])
            net_paths_list.append((net_uid, net_paths))
        self.nets_id_and_paths: List[tuple[int,List[str]]] = net_paths_list
        #TODO: does the new compiler provide a type for nets_paths?

    def process_ports(self, ports: List[ModelVertexView], is_inverted: bool = False) -> Port:
        """
        Provide a list of all ports associated to a component on the same net
        The function will return a Port object
        """
        #TODO: kind of a mess to figure out the pin direction. See if can be improved later.
        pin_adjacents_in: List[tuple[EdgeType, ModelVertexView]] = []
        neighbor_connected_pins_in: List[ModelVertexView] = []
        for port in ports:
            #TODO: the get_adjacents function is supposed to return a list but returns a zip object so need to cast to list. Might need to fix?
            pin_adjacents_in += list(port.get_adjacents_with_edge_types("in", EdgeType.connects_to))
        for pin_adjacent in pin_adjacents_in:
            # all the pins have the same parent, so testing element 0 only is enough
            # need to make sure that the parent of patent is the current module
            #TODO: this mechanism will not work if two signals are connected together
            if ports[0].parent_path != pin_adjacent[1].parent_path and (ports[0].parent.parent_path == pin_adjacent[1].parent.parent_path or ports[0].parent_path == pin_adjacent[1].parent.parent_path or ports[0].parent.parent_path == pin_adjacent[1].parent_path):
                neighbor_connected_pins_in.append(pin_adjacent[1])

        pin_adjacents_out: List[tuple[EdgeType, ModelVertexView]] = []
        neighbor_connected_pins_out: List[ModelVertexView] = []
        for port in ports:
            #TODO: the get_adjacents function is supposed to return a list but returns a zip object so need to cast to list
            pin_adjacents_out += list(port.get_adjacents_with_edge_types("out", EdgeType.connects_to))
        for pin_adjacent in pin_adjacents_out:
            # all the pins have the same parent, so testing element 0 only is enough
            # need to make sure that the parent of patent is the current module
            if ports[0].parent_path != pin_adjacent[1].parent_path and (ports[0].parent.parent_path == pin_adjacent[1].parent.parent_path or ports[0].parent_path == pin_adjacent[1].parent.parent_path or ports[0].parent.parent_path == pin_adjacent[1].parent_path):
                neighbor_connected_pins_out.append(pin_adjacent[1])

        # apparently that's how we do XORs
        #TODO: this seems broken for some reason
        if bool(is_inverted) != bool(len(neighbor_connected_pins_in) >= len(neighbor_connected_pins_out)):
            pin_direction = 'input'
        else:
            pin_direction = 'output'
        port_id = 0
        # the port id can be given based on element 0 only since we know they are all on the same net anyways
        for net in self.nets_id_and_paths:
            for pin_or_signal_path in net[1]:
                if ports[0].path == pin_or_signal_path:
                    port_id = net[0] #TODO: having a dict might make this more readable

        return Port(pin_direction, [port_id]) #TODO: I actually think this was not necessary based on the netlist standard


    def process_block(self, block: ModelVertexView) -> tuple[str, Cell]:
        # get all the pins, signals and interfaces part of that block
        return_list = block.get_adjacents("in", EdgeType.part_of)
        available_list: List[ModelVertexView] = []
        for element in return_list:
            element_type = element.vertex_type
            if (element_type == VertexType.pin or element_type == VertexType.signal or element_type == VertexType.interface):
                available_list.append(element)
        # create pin and signal clusters
        port_clusters: dict[int:List[ModelVertexView]] = {}
        for port_mvv in available_list:
            port_cluster: List[int, List[ModelVertexView]] = [0,[]]
            port_cluster[0] += generate_uid_from_path(port_mvv.path)
            port_cluster[1].append(port_mvv)
            connected_neighbors_list = port_mvv.get_adjacents("in", EdgeType.connects_to) + port_mvv.get_adjacents("out", EdgeType.connects_to)
            for con_neighbor in connected_neighbors_list:
                if con_neighbor.parent_path == port_mvv.parent_path:
                    port_cluster[0] += generate_uid_from_path(con_neighbor.path)
                    port_cluster[1].append(con_neighbor)
            # placing the clusters in the dict automatically removes duplicates
            port_clusters[port_cluster[0]] = port_cluster[1]

        # create named port cluster of the form 'p1,p2:sig1,sig2
        named_port_clusters: dict[str:List(ModelVertexView)] = {}
        for port_cluster in port_clusters:
            pin_names = []
            signal_names = []
            for port in port_clusters[port_cluster]:
                if port.vertex_type == VertexType.pin:
                    pin_names.append(port.ref)
                elif port.vertex_type == VertexType.signal:
                    signal_names.append(port.ref)

            cluster_name = join_pin_signal_str(make_list_friendly(pin_names), make_list_friendly(signal_names))

            named_port_clusters[cluster_name] = port_clusters[port_cluster]

        # process the pins, ...
        processed_port_clusters = {}
        for port_cluster_key in named_port_clusters:
            processed_port_clusters[port_cluster_key] = self.process_ports(named_port_clusters[port_cluster_key])

        output_port_dict = {}
        for port_cluster in processed_port_clusters:
            output_port_dict[port_cluster] = processed_port_clusters[port_cluster].direction

        output_connections = {}
        for port_cluster in processed_port_clusters:
            output_connections[port_cluster] = processed_port_clusters[port_cluster].bits

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
            port_list = [port]
            processed_port = self.process_ports(port_list, True)
            port_dict[port.ref] = processed_port

        # building the cell dict out
        cell_dict: dict[str:Cell] = {}
        for block in self.block_stack:
            cell = self.process_block(block)
            cell_dict[cell[0]] = cell[1]

        self.modules = Modules({'Vdiv':Module(port_dict,cell_dict)})
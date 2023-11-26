import datetime
import logging
from pathlib import Path
from contextlib import contextmanager
from typing import Any, Dict, List, Literal, Optional, TYPE_CHECKING, Iterable

import json
import hashlib
import uuid

from attrs import define, field, asdict

from atopile.model.accessors import ModelVertexView
from atopile.model.visitor import wander
from atopile.model.model import EdgeType, Model, VertexType
from atopile.targets.netlist.nets import find_nets, NetType
from atopile.targets.targets import Target, TargetCheckResult, TargetMuster

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

"""
Example Yosys netlist:
{
  "modules": {
    "voltage_divider": {
      "ports": {
        "vout": {
          "direction": "output",
          "bits": [ 2 ]
        }
      },
      "cells": {
        "r1": {
          "type": "r_v",
          "port_directions": {
            "A": "input",
            "B": "output"
          },
          "connections": {
            "A": [ 22222 ],
            "B": [ 3 ]
          }
        },
        "r2": {
          "type": "r_v",
          "port_directions": {
            "A": "input",
            "B": "output"
          },
          "connections": {
            "A": [ 3 ],
            "B": [ 4 ]
          }
        },
        "vcc": {
          "type": "vcc",
          "port_directions": {
            "A": "output"
          },
          "connections": {
            "A": [ 22222 ]
          }
        },
        "gnd": {
          "type": "gnd",
          "port_directions": {
            "A": "input"
          },
          "connections": {
            "A": [ 4 ]
          }
        }
      }
    }
  }
}
"""

@define
class Cell:
    type: str
    port_directions: Dict[str,str]
    connections: Dict[str,list]

@define
class Port:
    direction: str
    bits: list[str]

@define
class Module:
    ports: Dict[str, Port]
    cells: Dict[str, Cell]

@define
class Modules:
    modules: Dict[str, Module]

def make_list_friendly(things: Iterable[str]) -> str:
    return ",".join(thing for thing in things)

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

def resolve_port_cluster_name(port_cluster: List[ModelVertexView]) -> str:
    """
    return a port name of the form p1,p2:s1,s2
    """
    pin_names = []
    signal_names = []
    for port in port_cluster:
        if port.vertex_type == VertexType.pin:
            pin_names.append(port.ref)
        elif port.vertex_type == VertexType.signal:
            signal_names.append(port.ref)

    return join_pin_signal_str(make_list_friendly(pin_names), make_list_friendly(signal_names))

def _connections_within_module_layer(root_node, port_cluster: List[ModelVertexView], potential_pin_list: List[ModelVertexView]) -> str:
    neighbor_connected_pins: List[ModelVertexView] = []
    for pin_adjacent in potential_pin_list:
        # if parent path is root_node, the pin is a signal within the module and should be considered
        if pin_adjacent.parent_path == root_node:
            if pin_adjacent not in port_cluster:
                neighbor_connected_pins.append(pin_adjacent)
                #FIXME:print('selected: ', pin_adjacent.path)
        # all the pins have the same parent, so testing element 0 only is enough
        elif port_cluster[0].parent_path != pin_adjacent.parent_path:
            if pin_adjacent.parent.parent_path == root_node:
                neighbor_connected_pins.append(pin_adjacent)
                #FIXME:print('selected: ', pin_adjacent.path)
    return neighbor_connected_pins

def process_ports(root_node, nets_port_clusters, nets_id_and_paths, port_cluster: List[ModelVertexView], is_inverted: bool = False) -> Port:
    """
    When provided with a list of all ports associated to a component on the same net,
    this function will return a Port object
    """
    #TODO: kind of a mess to figure out the pin direction. See if can be improved later.
    pin_adjacents_in: List[tuple[EdgeType, ModelVertexView]] = []
    neighbor_connected_pins_in: List[ModelVertexView] = []
    for port in port_cluster:
        pin_adjacents_in += list(port.get_adjacents_with_edge_types("in", EdgeType.connects_to))
    neighbor_connected_pins_in = _connections_within_module_layer(root_node, port_cluster, [pin[1] for pin in pin_adjacents_in])

    pin_adjacents_out: List[tuple[EdgeType, ModelVertexView]] = []
    neighbor_connected_pins_out: List[ModelVertexView] = []
    for port in port_cluster:
        #TODO: the get_adjacents function is supposed to return a list but returns a zip object so need to cast to list
        pin_adjacents_out += list(port.get_adjacents_with_edge_types("out", EdgeType.connects_to))
    neighbor_connected_pins_out = _connections_within_module_layer(root_node, port_cluster, [pin[1] for pin in pin_adjacents_out])

    # apparently that's how we do XORs
    #TODO: this seems broken for some reason
    if bool(is_inverted) != bool(len(neighbor_connected_pins_in) >= len(neighbor_connected_pins_out)):
        pin_direction = 'input'
    else:
        pin_direction = 'output'

    port_id = 0
    # the port id can be given based on element 0 only since we know they are all on the same net anyways
    for net in nets_id_and_paths:
        for pin_or_signal_path in net[1]:
            if port_cluster[0].path == pin_or_signal_path:
                port_id = net[0] #TODO: having a dict might make this more readable

    return Port(pin_direction, [port_id]) #TODO: I actually think this was not necessary based on the netlist standard


def process_block(root_node, nets_ports_clusters, nets_id_and_paths, block: ModelVertexView) -> tuple[str, Cell]:
        # get all the pins, signals and interfaces part of that block
        return_list = block.get_adjacents("in", EdgeType.part_of)
        available_pin_signal_mvv_list: List[ModelVertexView] = []
        for element in return_list:
            element_type = element.vertex_type
            if (element_type == VertexType.pin or element_type == VertexType.signal): #TODO: add support for interface
                available_pin_signal_mvv_list.append(element)

        # create pin and signal clusters
        port_clusters: dict[int:List[ModelVertexView]] = {}
        port_already_clusterized: List[str] = []
        for port_mvv in available_pin_signal_mvv_list:
            for net_ports_clusters in nets_ports_clusters:
                for cluster_parent_path in net_ports_clusters:
                    if cluster_parent_path == port_mvv.parent_path:


            # for each port, we generate a map between a uid and all the signals and pins connected to it
            port_cluster: List[int, List[ModelVertexView]] = [0,[]]
            port_cluster[0] += generate_uid_from_path(port_mvv.path)
            port_cluster[1].append(port_mvv)
            connected_neighbors_list = port_mvv.get_adjacents("in", EdgeType.connects_to) + port_mvv.get_adjacents("out", EdgeType.connects_to)
            for con_neighbor in connected_neighbors_list:
                # if the port is part of the same component, add it to the cluster
                if con_neighbor.parent_path == port_mvv.parent_path:
                    port_cluster[0] += generate_uid_from_path(con_neighbor.path)
                    port_cluster[1].append(con_neighbor)
                    print('add port', con_neighbor.ref)
            # placing the clusters in the dict automatically removes duplicates
            port_clusters[port_cluster[0]] = port_cluster[1]

        # create named port cluster of the form 'p1,p2:sig1,sig2
        named_port_clusters: dict[str:List(ModelVertexView)] = {}
        cluster_name: str = ""
        for port_cluster in port_clusters:
            cluster_name = resolve_port_cluster_name(port_clusters[port_cluster])

            named_port_clusters[cluster_name] = port_clusters[port_cluster]
            print(cluster_name, ' : ', named_port_clusters[cluster_name])

        # process the pins, ...
        processed_port_clusters = {}
        for port_cluster_key in named_port_clusters:
            #FIXME: print('==========')
            # print('processing: ', port_cluster_key)
            processed_port_clusters[port_cluster_key] = process_ports(root_node, nets_id_and_paths, named_port_clusters[port_cluster_key])

        output_port_dict = {}
        for port_cluster in processed_port_clusters:
            output_port_dict[port_cluster] = processed_port_clusters[port_cluster].direction

        output_connections = {}
        for port_cluster in processed_port_clusters:
            output_connections[port_cluster] = processed_port_clusters[port_cluster].bits

        return (block.ref, Cell(block.ref, output_port_dict, output_connections))

conversion_function = lambda x: x.path

@define
class YosysNetlist():
    modules: Modules|None = None
    """
    Netlist is currently generated at a depth of a single module.
    This netlist is used in the context of visualisation through netlistsvg.
    """

    def to_file(self, path: Path) -> None:

        with path.open("w") as json_file:
            json.dump(asdict(self.modules), json_file)

    @classmethod
    def from_model(
        cls,
        model: Model,
        root_node: str,
        target: "YosysNetlistTarget",
    ) -> "YosysNetlist":
        # need to check that the node is of type module
        root_mvv = ModelVertexView.from_path(model, root_node)
        return_list = root_mvv.get_adjacents("in", EdgeType.part_of)

        block_stack:List[ModelVertexView] = []
        port_stack:List[ModelVertexView] = []
        nets_mvvs: List[NetType] = find_nets(model)
        nets_id_and_paths: Dict[int,List[str]] = []
        nets_port_clusters: List[Dict[ModelVertexView,List[ModelVertexView]]]

        # # for each net, we want a list of port paths as well as a unique identifier used for the netlist generation
        net_paths_list = []
        for net_mvvs in nets_mvvs:
            net_paths = list(map(conversion_function, net_mvvs))
            # we generate a uid from the first element in the list
            net_uid = generate_uid_from_path(net_paths[0])
            net_paths_list.append((net_uid, net_paths))
        nets_id_and_paths: List[tuple[int,List[str]]] = net_paths_list #TODO: change this to a dict

        for net_mvvs in nets_mvvs:
            net_clusters = {}
            for net_mvv in net_mvvs:
                net_clusters[net_mvv.parent_path].append(net_mvv)
            nets_port_clusters.append(net_clusters)

        # list all the components and modules within the module
        for element in return_list:
            if element.vertex_type == VertexType.module or element.vertex_type == VertexType.component:
                block_stack.append(element)

        # list all the signals and interfaces within the module
        for element in return_list:
            if element.vertex_type == VertexType.signal or element.vertex_type == VertexType.interface:
                port_stack.append(element)

        # building the port dict out
        port_dict = {}
        for port in port_stack:
            port_list = [port]
            processed_port = process_ports(root_node, nets_port_clusters, nets_id_and_paths,port_list, True)
            port_dict[port.ref] = processed_port

        # building the cell dict out
        cell_dict: dict[str:Cell] = {}
        for block in block_stack:
            cell = process_block(root_node, nets_port_clusters,nets_id_and_paths, block)
            cell_dict[cell[0]] = cell[1]

        netlist = YosysNetlist(
            modules = Modules({root_node:Module(port_dict,cell_dict)})
        )

        return netlist

class YosysNetlistTarget(Target):
    name = "netlist-yosys"
    def __init__(self, muster: TargetMuster) -> None:
        self._netlist: Optional[YosysNetlist] = None
        super().__init__(muster)

    def generate(self) -> YosysNetlist:
        if self._netlist is None:
            self._netlist = YosysNetlist.from_model(
                self.model,
                root_node=self.build_config.root_node,
                target=self,
            )
        return self._netlist

    def check(self) -> TargetCheckResult:
        #TODO: fix this in the future
        return True

    def check_has_been_run(self) -> bool:
        #TODO: fix this too
        return True

    def build(self) -> None:
        netlist = self.generate()
        output_file = self.build_config.build_path / self.build_config.root_file.with_suffix(".yosys.json").name
        netlist.to_file(output_file)

    def resolve(self, *args, clean=None, **kwargs) -> None:
        log.info(f"No direct resolve action for {self.name}")
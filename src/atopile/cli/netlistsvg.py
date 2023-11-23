import logging
from contextlib import contextmanager
from typing import Any, Dict, List, Literal, Optional, TYPE_CHECKING, Iterable

import click
import json
import uvicorn
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
    bits: str
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



class Roley(ModelVisitor):
    def __init__(self, model: Model) -> None:
        self.model = model
        self.all_verticies: List[ModelVertexView] = []
        self.block_stack: List[ModelVertexView] = []
        self.modules: Modules
        super().__init__(model)

    def process_port(self, port: ModelVertexView) -> tuple(str, Port):
        pin_adjacents = list(port.get_adjacents_with_edge_types("in", EdgeType.connects_to)) + list(port.get_adjacents_with_edge_types("out", EdgeType.connects_to))
        neighbor_connected_pins: List[mvv]
        for pin_adjacent in pin_adjacents:
            if port.parent_path != pin_adjacent[1].parent_path:
                consumed_list.append((element, pin_adjacent[1]))


    def process_block(self, block: ModelVertexView) -> tuple(str, Cell):
        # get all the pins, signals and interfaces part of that block
        return_list = block.get_adjacents("in", EdgeType.part_of)
        available_list: List[ModelVertexView] = []
        for element in return_list:
            element_type = element.vertex_type
            if (element_type == VertexType.pin or element_type == VertexType.signal or element_type == VertexType.interface):
                available_list.append(element)
        # process the pins, ...
        port_dict: {str:Port} = {}
        for element in available_list:
            port = self.process_port(element)


    def build_netlist(self, root_node) -> Modules:
        # need to check that the node is of type module
        root_mvv = ModelVertexView.from_path(self.model, root_node)
        return_list = root_mvv.get_adjacents("in", EdgeType.part_of)
        for element in return_list:
            if element.vertex_type == VertexType.module or element.vertex_type == VertexType.component:
                self.block_stack.append()
        cell_dict = {}
        for block in self.block_stack:
            cell = self.process_block(block)
            cell_dict[cell[0]] = cell[1]
        




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
    print(project.module_dir)
    # Putting this as a trial
    root_node = "vdiv.ato:Vdiv"
    root_mvv = ModelVertexView.from_path(model, root_node)

    cell = Cell('r_v', {'A':'input', 'B':'output'}, {'A': [2], 'B': [2]})
    cell_2 = Cell('r_v', {'A':'input', 'B':'output'}, {})
    port = Port('output', [2])
    module = Module({'vout':attrs.asdict(port)},{'r1': attrs.asdict(cell), 'r2':attrs.asdict(cell_2)})
    module_1 = Modules({'vdiv' : module})

    with open("data.json", "w") as json_file:
        json.dump(attrs.asdict(module_1), json_file)



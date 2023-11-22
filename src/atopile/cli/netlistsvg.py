import logging
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
class Cell:
    # mandatory external
    type: str
    port_dimensions: dict[str:str]
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
        super().__init__(model)



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
    port = Port('output', [2])
    module = Module({'vout':attrs.asdict(port)},{'r1': attrs.asdict(cell)})
    module_1 = Modules({'vdiv' : module})

    with open("data.json", "w") as json_file:
        json.dump(attrs.asdict(module_1), json_file)



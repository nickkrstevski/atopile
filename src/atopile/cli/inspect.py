import logging

import click
import uvicorn
from atopile.project.project import Project
from atopile.project.config import BuildConfig
from atopile.cli.common import ingest_config_hat
from atopile.parser.parser import build_model
from atopile.model.accessors import ModelVertexView
from atopile.model.model import EdgeType, VertexType

from rich.console import Console
from rich.table import Table

# configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


# configure UI
@click.command()
@ingest_config_hat
@click.option("--debug/--no-debug", default=False)
def inspect(
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
    # Putting this as a trial
    root_node = "buck_reg.ato:BuckReg.buck_converter"
    root_mvv = ModelVertexView.from_path(model, root_node)
    return_list = root_mvv.get_adjacents("in", EdgeType.part_of)
    pin_list = []
    signal_list = []
    interface_list = []
    for element in return_list:
        element_type = element.vertex_type
        if element_type == VertexType.interface:
            interface_list.append(element)
        elif element_type == VertexType.signal:
            signal_list.append(element)
        elif element_type == VertexType.pin:
            pin_list.append(element)

    table = Table(title="Available pins on component")

    table.add_column("Pin #", justify="center", style="cyan", no_wrap=True)
    table.add_column("Signals",  justify="center", style="magenta")
    table.add_column("Interfaces", justify="center", style="green")

    table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690")
    table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347")
    table.add_row("Dec 15, 2017", "Star Wars Ep. V111: The Last Jedi", "$1,332,539,889")
    table.add_row("Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,332,439,889")

    console = Console()
    console.print(table)

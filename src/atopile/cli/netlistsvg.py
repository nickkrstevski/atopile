import logging
from contextlib import contextmanager

import click
import json

import attrs as attrs

from atopile.cli.common import ingest_config_hat
from atopile.parser.parser import build_model
from atopile.project.config import BuildConfig
from atopile.project.project import Project
from atopile.viewer.netlist_generator import Roley

# configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


# configure UI
@click.command()
@ingest_config_hat
@click.option("--debug/--no-debug", default=False)
def netlistsvg(
    project: Project, build_config: BuildConfig, debug: bool
):
    """
    Generate a netlist in a yosys format based on the model
    eg. `ato netlistsvg path/to/source.ato:module.path`
    """

    if debug:
        # FIXME: Do we need this?
        import atopile.parser.parser

        atopile.parser.parser.log.setLevel(logging.DEBUG)

    # build core model
    model = build_model(project, build_config)

    on_a_roll = Roley(model)
    on_a_roll.build_netlist(build_config.root_node)

    with open("data.json", "w") as json_file:
        json.dump(attrs.asdict(on_a_roll.modules), json_file)



import logging

import click
<<<<<<< HEAD
from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme

from . import build, create, install

console = Console(
    theme=Theme({"logging.level.warning": "yellow"})
)


=======
from rich.logging import RichHandler

from atopile.cli.rich_console import console

from . import build, create, install

>>>>>>> origin/main
FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO",
    format=FORMAT,
    datefmt="[%X]",
    handlers=[
        RichHandler(
            console=console,
            tracebacks_suppress=[click],
        )
    ]
)


# cli root
@click.version_option()
@click.group()
def cli():
    pass


cli.add_command(build.build)
cli.add_command(create.create)
cli.add_command(install.install)


if __name__ == "__main__":
    cli()

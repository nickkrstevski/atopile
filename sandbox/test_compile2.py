from atopile.parser.parser2 import parse
from pathlib import Path
from atopile.model2.compile import compile

import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger(__name__)
log.info("Hello, World!")

res_path = Path("/Users/mattwildoer/Projects/atopile-workspace/atopile/src/standard_library/std/resistor.ato")

tree = list(parse([res_path]).values())[0]

log.info("Compiling...")
compile(res_path, tree, log)

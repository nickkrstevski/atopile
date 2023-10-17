from atopile.parser.parser2 import parse
from pathlib import Path

import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")
log.info("Hello, World!")

if __name__ == "__main__":
    parse(Path("/Users/mattwildoer/Projects/atopile-workspace/servo-drive/elec/src").glob("**/*.ato"))

#%%
# reimport modules on rerun with jupyter
%load_ext autoreload
%autoreload 2
from atopile.parser.parser2 import parse
from atopile.deps import DependencySolver, PathFinder
from pathlib import Path
from atopile.model2.compile import compile_file
from concurrent.futures import ThreadPoolExecutor

import logging
from rich.logging import RichHandler
from rich.tree import Tree
import rich
from itertools import chain

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")
log.info("Hello, World!")

#%%
finder = PathFinder(
    [
        Path("/Users/mattwildoer/Projects/atopile-workspace/servo-drive/elec/src"),
        Path("/Users/mattwildoer/Projects/atopile-workspace/atopile/src/standard_library"),
    ]
)

#%%
asts = parse(finder.glob("**/*.ato"))

#%%
dependency_solver = DependencySolver.from_asts(
    finder.find,
    asts
)

# %%
file = Path("/Users/mattwildoer/Projects/atopile-workspace/servo-drive/elec/src/vdiv.ato")
vdiv_deps = DependencySolver.from_dm_and_path(dependency_solver, file)

#%%
built = {}
for p in vdiv_deps.build_order():
    built[p] = compile_file(p, asts[p], built, finder.find)

# %%

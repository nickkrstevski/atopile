from antlr4.tree.Trees import Trees
from unittest.mock import MagicMock
import pytest
from atopile.dev.parse import parse_file
from atopile.model2.datamodel1 import Object, Link, Import, Replace, MODULE, COMPONENT, PIN, SIGNAL, INTERFACE
from rich.tree import Tree
from rich import print
from atopile.dev.dm1_vis import Wendy

# =========================
# test individual functions
# =========================


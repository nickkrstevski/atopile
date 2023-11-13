from atopile.dev.parse import parse_as_file, make_parser
from atopile.model2.datamodel1 import Object, Link, Import, Dizzy, Type, Replace
from atopile.model2.datamodel1 import MODULE, COMPONENT, PIN, SIGNAL, INTERFACE
from atopile.parser.AtopileParserVisitor import AtopileParserVisitor
from atopile.model2 import errors
from antlr4.tree.Trees import Trees
from unittest.mock import MagicMock
import pytest



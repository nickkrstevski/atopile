from atopile.dev.parse import parse_as_file, make_parser
from atopile.model2.datamodel1 import (
    Object, Link, Import, Dizzy, Type,
    Replace, MODULE, COMPONENT, PIN, SIGNAL, INTERFACE
)
from atopile.parser.AtopileParserVisitor import AtopileParserVisitor
from atopile.model2.datamodel2 import Scoop, Lofty
from atopile.model2 import errors
from unittest.mock import MagicMock
import pytest


def test_():
    tree = parse_as_file(
        """
        component comp1:
            signal a
        component comp2 from comp1:
            signal b
        """
    )
    dizzy = Dizzy("test.ato")
    dm1_tree = dizzy.visitFile_input(tree)

    scoop = Scoop()
    scoop.visit_roots([dm1_tree])

    lofty = Lofty(
        dm1_id_object_map=scoop.dm1_id_object_map,
        dm1_id_name_binding_map=scoop.dm1_id_name_binding_map,
        dm1_id_closure_map=scoop.dm1_id_closure_map,
        search_paths=[],
        path_dm1_map={"test.ato": dm1_tree},
    )
    dm2_tree = list(lofty.visit_roots([dm1_tree]))[0]
    dm2_tree

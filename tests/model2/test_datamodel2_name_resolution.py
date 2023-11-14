from contextlib import nullcontext
from typing import Any, Optional
from unittest.mock import MagicMock

import pytest
from atopile.dev.parse import make_parser, parse_as_file
from atopile.model2 import datamodel1 as dm1
from atopile.model2 import errors
from atopile.model2.datamodel2 import Lofty, Scoop
from atopile.parser.AtopileParserVisitor import AtopileParserVisitor


@pytest.mark.parametrize(
    (   "scope"    , "ref"          , "abs_ref"      , "value", "ex"),
    (
        (None      , tuple()        , tuple()        , None   , None     ),  # empty refs point to self
        (None      , ("z",)         , None           , None   , KeyError ),  # unbound name
        (None      , ("h",)         , ("h",)         , None   , None     ),  # bound name
        (None      , ("h", "i")     , None           , None   , KeyError ),  # nested unbound name
        (None      , ("a", "b", "c"), ("a", "b", "c"), None   , None     ),  # nested bound name
        (None      , ("i", "j")     , None           , None   , TypeError),  # bound name in global scope
        (("a",)    , ("b",)         , ("a", "b")     , None   , None     ),  # bound name in parent scope
        (("a", "b"), ("c",)         , ("a", "b", "c"), None   , None     ),  # bound name in nested parent scope
        (("a", "b"), ("e",)         , ("e",)         , None   , None     ),  # bound name in closure
        (("a", "b"), ("e", "f")     , ("e", "f")     , None   , None     ),  # nested bound name in closure
        (("e",)    , ("a", "b", "c"), None           , 10     , None     ),  # overriden bound name in closure
        (("e",)    , ("a", "b")     , ("a", "b")     , None   , None     ),  # overriden bound name in closure
        (("e", "p"), ("a", "b", "c"), None           , 10     , None     ),  # overriden bound name in closure
    ),
)
def test_in_scope(
    scope: dm1.Ref,
    ref: dm1.Ref,
    abs_ref: dm1.Ref,
    value: Optional[Any],
    ex: Optional[Exception],
):
    tree = parse_as_file(
        """
        module a:
            module b:
                signal c
                signal d
        module e:
            signal f
            signal g
            a.b.c = 10
            module p:
                signal q
        signal h
        i = 10
        """
    )
    dizzy = dm1.Dizzy("test.ato")
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

    scope_obj = dm1_tree if scope is None else lofty.find_in_scope_dm1(scope, dm1_tree)

    if ex is not None:
        with pytest.raises(ex):
            lofty.find_in_scope_dm1(ref, scope_obj)
        return  # we pass here
    else:
        val = lofty.find_in_scope_dm1(ref, scope_obj)

    if abs_ref is not None:
        assert val is lofty.find_in_scope_dm1(abs_ref, dm1_tree)
    elif value is not None:
        assert val == value
    else:
        raise ValueError("bad test case")

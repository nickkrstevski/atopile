import pyparsing as pp
import pytest
from copy import copy
from . import generic
from . import ast

def test_identifier():
    id = generic.identifier
    # valid identifiers
    assert id.parseString('test_identifier3').as_list() == ['test_identifier3']
    assert id.parseString('_test_identifier3').as_list() == ['_test_identifier3']

    # invalid identifiers
    with pytest.raises(pp.ParseException):
        id.parseString('4test_identifier').as_list()

def test_path():
    path = generic.path
    assert path.parse_string('test.path27.asdf').as_list() == ['test', 'path27', 'asdf']

def test_reference():
    ref = generic.reference
    dummy = ast.Reference(
        source=None,
        locn_start=0,
        locn_end=0,
        path=[],
    )

    # valid references
    basic_id = copy(dummy)
    basic_id.path = ['test_identifier3']
    basic_id.locn_end = len(basic_id.path[0])
    assert ref.parseString('test_identifier3').as_list() == [basic_id]

    path_ref = copy(dummy)
    path_ref.path = ['test', 'path27', 'asdf']
    path_ref.locn_end = len(basic_id.path[0])
    assert ref.parseString('test.path27.asdf').as_list() == [path_ref]


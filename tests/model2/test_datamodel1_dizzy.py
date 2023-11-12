from ..utils import parse, make_parser
from atopile.model2.datamodel1 import Object, Link, Import, Dizzy, Type, compile_file
from atopile.model2.datamodel1 import MODULE, COMPONENT, PIN, SIGNAL, INTERFACE
from atopile.parser.AtopileParserVisitor import AtopileParserVisitor
from atopile.model2 import errors
from antlr4 import *
from antlr4.tree.Trees import Trees
from unittest.mock import MagicMock
import pytest

# =========================
# test individual functions
# =========================

# test Totally_an_integer
@pytest.mark.parametrize(
    "input",
    [
        "1.1",
        "hello",
        "False",
        "None",
        "True",
        "true",
        "false"
    ]
)
def test_Totally_an_integer_errors(input):
    mock_ctx = MagicMock()
    getText = MagicMock()
    getText.return_value = input
    mock_ctx.getText = getText

    with pytest.raises(errors.AtoTypeError):
        dizzy = Dizzy("test.ato")
        dizzy.visitTotally_an_integer(mock_ctx)


@pytest.mark.parametrize(
    ("input", "output"),
    [
        ("0", 0),
        ("1", 1),
        ("5", 5),
    ]
)
def test_Totally_an_integer_passes(input, output):
    mock_ctx = MagicMock()
    getText = MagicMock()
    getText.return_value = input
    mock_ctx.getText = getText

    dizzy = Dizzy("test.ato")
    assert output == dizzy.visitTotally_an_integer(mock_ctx)

# test visitName
@pytest.mark.parametrize(
    ("input", "output"),
    [
        ("0", (0,)),
        ("1", (1,)),
        ("5", (5,)),
        ('hello', ("hello",))
    ]
)
def test_visitName(input, output):
    mock_ctx = MagicMock()
    getText = MagicMock()
    getText.return_value = input
    mock_ctx.getText = getText

    dizzy = Dizzy("test.ato")
    assert output == dizzy.visitName(mock_ctx)

#TODO: check for a..b error at model 1 level
def test_visitAttr():
    parser = make_parser("a.b.c")
    ctx = parser.attr()

    dizzy = Dizzy("test.ato")
    assert (('a',), ('b',), ('c',)) == dizzy.visitAttr(ctx)

# =============
# test compiler
# =============

def test_visitSignaldef_stmt():
    parser = make_parser("signal signal_a")
    ctx = parser.signaldef_stmt()

    dizzy = Dizzy("test.ato")
    ret = dizzy.visitSignaldef_stmt(ctx)
    assert ret == (('signal_a',), Object(supers=(SIGNAL)))


def test_visitPindef_stmt():
    parser = make_parser("pin pin_a")
    ctx = parser.pindef_stmt()

    dizzy = Dizzy("test.ato")
    ret = dizzy.visitPindef_stmt(ctx)
    assert ret == (('pin_a',), Object(supers=(PIN)))


def test_visitConnect_stmt_simple():
    parser = make_parser("pin_a ~ pin_b")
    ctx = parser.connect_stmt()

    dizzy = Dizzy("test.ato")
    ret = dizzy.visitConnect_stmt(ctx)
    assert ret == ((None, Link(source=('pin_a',), target=('pin_b',))),)

def test_visitConnect_stmt_instance():
    parser = make_parser("pin pin_a ~ signal sig_b")
    ctx = parser.connect_stmt()

    dizzy = Dizzy("test.ato")
    ret = dizzy.visitConnect_stmt(ctx)
    assert ret == ((None, Link(source=('pin_a',), target=('sig_b',))), (('pin_a',), Object(supers=(PIN))), (('sig_b',), Object(supers=(SIGNAL))),)

def test_visitImport_stmt():
    parser = make_parser("import Module1 from 'test_import.ato'")
    ctx = parser.import_stmt()

    dizzy = Dizzy("test.ato")
    ret = dizzy.visitImport_stmt(ctx)
    assert ret == ((None, Import(what=('Module1',), from_='test_import.ato')))

def test_visitBlockdef():
    parser = make_parser(
        """component comp1 from comp2:
            signal signal_a
        """
    )
    ctx = parser.compound_stmt()

    dizzy = Dizzy("test.ato")
    results = dizzy.visitCompound_stmt(ctx)
    assert results == (
        ('comp1',), Object(supers=(COMPONENT,('comp2',)),
        locals_= (('signal_a',), Object(supers=(SIGNAL)))
        ))

def test_visitAssign_stmt_value():
    parser = make_parser("foo.bar = 35")
    ctx = parser.assign_stmt()

    dizzy = Dizzy("test.ato")
    results = dizzy.visitAssign_stmt(ctx)
    assert results == ((('foo',), ('bar',)), 35)

def test_visitAssign_stmt_string():
    parser = make_parser('foo.bar = "baz"')
    ctx = parser.assign_stmt()

    dizzy = Dizzy("test.ato")
    results = dizzy.visitAssign_stmt(ctx)
    assert results == ((('foo',), ('bar',)), "baz")

def test_visitModule1LayerDeep():
    tree = parse(
        """
        component comp1:
            signal signal_a
            signal signal_b
            signal_a ~ signal_b
        """
    )
    dizzy = Dizzy("test.ato")
    results = dizzy.visitFile_input(tree)
    assert results == [
        (('comp1',), Object(supers=(COMPONENT),
        locals_= (
            (('signal_a',), Object(supers=(SIGNAL))),
            (('signal_b',), Object(supers=(SIGNAL))),
            ((None, Link(source=('signal_a',), target=('signal_b',))),),)
        ))
    ]


def test_visitModule2LayerDeep():
    tree = parse(
        """
        module mod1:
            component comp1:
                signal signal_a
                signal signal_a
        """
    )
    dizzy = Dizzy("test.ato")
    results = dizzy.visitFile_input(tree)
    print(results)
    assert results == [
        (('mod1',), Object(supers=(MODULE), locals_= (
            (('comp1',), Object(supers=(COMPONENT),locals_= (
                (('signal_a',), Object(supers=(SIGNAL))),
                (('signal_a',), Object(supers=(SIGNAL))),)
            ))
        )))
    ]

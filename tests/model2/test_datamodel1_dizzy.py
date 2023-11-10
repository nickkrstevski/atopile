from ..utils import parse
from atopile.model2.datamodel1 import Object, Dizzy, Type, compile_file
from atopile.model2.datamodel1 import MODULE, COMPONENT, PIN, SIGNAL, INTERFACE
from atopile.parser.AtopileParserVisitor import AtopileParserVisitor
from atopile.model2 import errors
from antlr4 import *
from antlr4.tree.Trees import Trees
from unittest.mock import MagicMock
import pytest


def test_visitSignaldef_stmt():
    tree = parse(
        """
        signal signal_a
        """
    )
    dizzy = Dizzy("test.ato")
    ret = dizzy.visitFile_input(tree)
    assert ret == [('signal_a', Object(supers=(SIGNAL)))]


def test_visitModule1LayerDeep():
    tree = parse(
        """
        component comp1:
            signal signal_a
            signal signal_a
        """
    )
    # print('start test')
    dizzy = Dizzy("test.ato")
    results = dizzy.visitFile_input(tree)
    assert results == [
        ('comp1', Object(supers=(COMPONENT),locals_= (
            ('signal_a', Object(supers=(SIGNAL))),
            ('signal_a', Object(supers=(SIGNAL))),)
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
    # print('start test')
    dizzy = Dizzy("test.ato")
    results = dizzy.visitFile_input(tree)
    print(results)
    assert results == [
        ('mod1', Object(supers=(MODULE), locals_= (
            ('comp1', Object(supers=(COMPONENT),locals_= (
                ('signal_a', Object(supers=(SIGNAL))),
                ('signal_a', Object(supers=(SIGNAL))),)
            ))
        )))
    ]


def test_visitPindef_stmt():
    tree = parse(
        """
        pin pin_a
        """
    )
    dizzy = Dizzy("test.ato")
    ret = dizzy.visitFile_input(tree)
    assert ret == [('pin_a', Object(supers=(PIN)))]


def test_visitConnect_stmt():
    tree = parse(
        """
        module mod1:
            pin_a ~ pin_b
        """
    )
    dizzy = Dizzy("test.ato")
    ret = dizzy.visitFile_input(tree)
    assert ret == [('pin_a', Object(supers=(PIN)))]


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

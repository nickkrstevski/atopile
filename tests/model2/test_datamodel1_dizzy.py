from ..utils import parse
from atopile.model2.datamodel1 import Object, Dizzy, Type, compile_file
from atopile.model2.datamodel1 import MODULE, COMPONENT, PIN, SIGNAL, INTERFACE
from atopile.parser.AtopileParserVisitor import AtopileParserVisitor
from antlr4 import *
from antlr4.tree.Trees import Trees

def test_visitSignaldef_stmt():
    tree = parse(
        """
        signal signal_a
        """
    )
    dizzy = Dizzy("test.ato")
    ret = dizzy.visitFile_input(tree)
    assert ret == [('signal_a', Object(supers=[SIGNAL]))]

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
        ('comp1', Object(supers=[COMPONENT],locals_= (
            ('signal_a', Object(supers=[SIGNAL])),
            ('signal_a', Object(supers=[SIGNAL])),)
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
        ('mod1'), Object(supers=(MODULE), locals_= (
            ('comp1', Object(supers=(COMPONENT),locals_= (
                ('signal_a', Object(supers=(SIGNAL))),
                ('signal_a', Object(supers=(SIGNAL))),)
            ))
        ))
    ]

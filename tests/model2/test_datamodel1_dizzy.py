from ..utils import parse
from atopile.model2.datamodel1 import Dizzy, compile_file
from antlr4 import *
from antlr4.tree.Trees import Trees

# TODO: write some tests!

def test_datamodel1():
    tree = parse(
        """
        component comp1:
            signal signal_a
            signal signal_b
            signal_a ~ pin 1
        """
    )
    # print('start test')
    dizzy = Dizzy("test.ato")
    results = dizzy.visitFile_input(tree)
    for result in results:
        print(result)
    # print(Trees.toStringTree(tree))
    # print(compile_file(tree))
    # print('hello00')

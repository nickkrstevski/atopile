import antlr4
from atopile.language.generated.AtopileLexer import AtopileLexer
from atopile.language.generated.AtopileParser import AtopileParser
from atopile.language.generated.AtopileVisitor import AtopileVisitor

input_stream = antlr4.InputStream("""
from std import I2C;

block SomeBlock() {
    signal vcc;
    signal gnd;

    feature i2c() from I2C() {}
}
""")
lexer = AtopileLexer(input_stream)
token_stream = antlr4.CommonTokenStream(lexer)
parser = AtopileParser(token_stream)

# Parse the input and get the parse tree
tree = parser.file_input()

# Print the parse tree in the LISP-style string format
print(tree.toStringTree(recog=parser))

class Visitor(AtopileVisitor):
    def __init__(self) -> None:
        super().__init__()

    # Visit a parse tree produced by AtopileParser#import_statement.
    def visitImport_statement(self, ctx: AtopileParser.Import_statementContext):
        ctx_dict = [c.getText() for c in ctx.children]
        print(f"hit import! {ctx_dict}")
        return self.visitChildren(ctx)

visitor = Visitor()
visitor.visit(tree)

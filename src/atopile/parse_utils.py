"""
Utils related to handling the parse tree
"""
from pathlib import Path

from antlr4 import InputStream, ParserRuleContext, ParseTreeVisitor, Token, TerminalNode


def get_src_info_from_token(token: Token) -> tuple[str, int, int]:
    """Get the source path, line, and column from a context"""
    input_stream: InputStream = token.getInputStream()
    return input_stream.name, token.line, token.column


def get_src_info_from_ctx(ctx: ParserRuleContext) -> tuple[str | Path, int, int, int, int]:
    """Get the source path, line, and column from a context"""
    token: Token = ctx.start
    _, stop_line, stop_char = get_src_info_from_token(ctx.stop)
    return *get_src_info_from_token(token), stop_line, stop_char


# FIXME: I hate this pattern
# It should instead at least return a list of tokens
# for processing in a regular for loop
class _Reconstructor(ParseTreeVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.txt = ""
        self.last_line = None
        self.last_col = None

    def visitTerminal(self, node) -> str:
        symbol: Token = node.getSymbol()

        if self.last_line is None:
            self.last_line = symbol.line
            self.last_col = symbol.start

        if symbol.line > self.last_line:
            self.txt += "\n" * (symbol.line - self.last_line)
            self.last_col = 0

        self.txt += " " * (symbol.start - self.last_col - 1)

        self.last_line = symbol.line
        self.last_col = symbol.stop

        self.txt += node.getText()
        return super().visitTerminal(node)


def reconstruct(ctx: ParserRuleContext) -> str:
    """Reconstruct the source code from a parse tree"""
    reco = _Reconstructor()
    reco.visit(ctx)
    return reco.txt

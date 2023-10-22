from antlr4 import ParserRuleContext
from atopile.model2.parse import parse_text
from textwrap import dedent


def parse(src_code: str, src_path: str = "test.ato") -> ParserRuleContext:
    return parse_text(src_path, dedent(src_code))

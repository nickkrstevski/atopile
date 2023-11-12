import logging
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager, nullcontext
from pathlib import Path
from textwrap import dedent
from typing import Iterable, Iterator

from antlr4 import CommonTokenStream, InputStream, ParserRuleContext
from antlr4.error.ErrorListener import ErrorListener
from antlr4.ParserRuleContext import ParserRuleContext
from rich.progress import Progress

from atopile.model2.errors import AtoSyntaxError
from atopile.model2.parse import parser_of_text
from atopile.parser.AtopileLexer import AtopileLexer
from atopile.parser.AtopileParser import AtopileParser
from atopile.utils import profile as profile_within

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class ParserErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise AtoSyntaxError(f"Syntax error: '{msg}'", line, column)


def make_parser(src_code: str) -> AtopileParser:
    input = InputStream(dedent(src_code))

    lexer = AtopileLexer(input)
    stream = CommonTokenStream(lexer)
    parser = AtopileParser(stream)

    error_listener = ParserErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)

    return parser


def parse_file(src_code: str) -> ParserRuleContext:
    parser = make_parser(src_code)
    return parser.file_input()

tree = parse_file(
    """
    module mod1:
        component comp1:
            signal signal_a
            signal signal_a
    """
)
print(repr(tree))
"""
Parser elements for pin definitions
"""
import pyparsing as pp
from . import generic
from . import ast

# operators
connection_operator = pp.oneOf("~")
assignment_operator = pp.Literal("=")

def make_pin(s, loc, tokens):
    return ast.Pin(
        source=None,
        locn_start=loc,
        locn_end=loc + len(s),
        name=tokens['name'],
        connections=tokens['connections'],
    )

pin_defintion = (
    pp.Keyword('pin') +
    generic.identifier.set_results_name('name') +
    pp.Optional(
        pp.Suppress(connection_operator) +
        pp.delimited_list(generic.reference, delim=","),
        default=None
    ).set_results_name('connections')
).set_parse_action(make_pin)

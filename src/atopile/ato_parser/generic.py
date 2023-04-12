import pyparsing as pp
from . import ast

dot = pp.Literal('.')

identifier = pp.Word(pp.alphas + "_", pp.alphanums + "_")
value = pp.Word(pp.nums + ".", pp.alphas)
comment = pp.python_style_comment

path = pp.Combine(identifier + pp.ZeroOrMore(dot + identifier))

def make_reference(s, loc, tokens):
    return ast.Reference(
        source=None,
        locn_start=loc,
        locn_end=loc + len(s),
        path=tokens.as_list(),
    )

reference = (path | identifier).set_parse_action(make_reference)



#%%
# # eg. V[abc]
# # eg. V[abc:pqr]
# real_identifier = pp.Group(identifier + "[" + pp.Group(value + pp.Optional(":" + value)) + "]")

# #%%


# generic_assignment = pp.Group(identifier + assignment_operator + value)
# model_definition = pp.Group(identifier + assignment_operator + value)

# bracketed_expression = pp.nestedExpr(opener="(", closer=")", content=pp.delimitedList(generic_assignment, delim=","))
# limit_expression = pp.Group("limit" + pp.delimitedList(value + comparison_operator + value + comparison_operator + value, delim=","))
# feature_declaration = pp.Group("feature" + identifier + pp.Optional("(" + pp.delimitedList(identifier) + ")") + ":")
# component_declaration = pp.Group("component:")

# def parse_feature(s, loc, toks):
#     return datamodel.Feature(pins=[], transfer_functions=[], limits=[], states=[])

# def parse_component(s, loc, toks):
#     return datamodel.Component(pins=[], transfer_functions=[], types=[], limits=[], states=[], features=[])

# feature_declaration.setParseAction(parse_feature)
# component_declaration.setParseAction(parse_component)

# language = pp.ZeroOrMore(feature_declaration | component_declaration)

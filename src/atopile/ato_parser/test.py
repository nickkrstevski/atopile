import pyparsing as pp

# Define the parser
identifier = pp.Word(pp.alphas, pp.alphanums + "_")
dot = pp.Suppress(pp.Literal('.'))
dot_accessor = pp.Group(identifier + pp.ZeroOrMore(dot + identifier))

# Test the parser
valid_example = "a.b.c"
invalid_example = "a .b.c"

parsed_valid = dot_accessor.parseString(valid_example)
print(parsed_valid[0])

try:
    parsed_invalid = dot_accessor.parseString(invalid_example)
    print(parsed_invalid[0])
except pp.ParseException as e:
    print(f"Failed to parse: {e}")

from lark_parser import parseTree

grammar = open("grammar.lark", 'r').read()
code = open("examples/only-expressions.wan", 'r').read()

tree = parseTree(grammar, code)
print(tree.pretty())

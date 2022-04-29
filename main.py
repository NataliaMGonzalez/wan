from lark_parser import parseTree

grammar = open("grammar.lark", 'r').read()
code = open("example.wan", 'r').read()

tree = parseTree(grammar, code)
print(tree.pretty())

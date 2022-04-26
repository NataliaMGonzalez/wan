from lark_parser import parseTree
from pprint import PrettyPrinter
from variables_table import generate_variables_table

grammar = open("grammar.lark", 'r').read()
code = open("examples/only-expressions.wan", 'r').read()

tree = parseTree(grammar, code)

variables_table = generate_variables_table(tree)
PrettyPrinter().pprint(variables_table)

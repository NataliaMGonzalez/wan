from lark_parser import parseTree
from pprint import PrettyPrinter
from variables_table import generate_variables_table
from functions_directory import generate_functions_directory
from quadruples_linear_statements import generate_quadruples

grammar = open("grammar.lark", 'r').read()
code = open("examples/only-expressions.wan", 'r').read()

tree = parseTree(grammar, code)
print(tree.pretty())

variables_table = generate_variables_table(tree)
PrettyPrinter().pprint(variables_table)

quadruples = generate_quadruples(tree)
print("quadruples: ")
print(*quadruples, sep = "\n")

functions_directory = generate_functions_directory(tree)
PrettyPrinter().pprint(functions_directory)

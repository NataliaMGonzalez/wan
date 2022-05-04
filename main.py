from lark_parser import parseTree
from pprint import PrettyPrinter
from variables_table import generate_variables_table
from functions_directory import generate_functions_directory

grammar = open("grammar.lark", 'r').read()
code = open("examples/full-functionality.wan", 'r').read()

tree = parseTree(grammar, code)

variables_table = generate_variables_table(tree)
PrettyPrinter().pprint(variables_table)

functions_directory = generate_functions_directory(tree)
PrettyPrinter().pprint(functions_directory)

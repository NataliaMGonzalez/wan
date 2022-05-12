from lark_parser import parseTree
from pprint import PrettyPrinter
from variables_table import generate_variables_table
from functions_directory import generate_functions_directory
from quadruples import generate_quadruples
from memory_manager import memory

grammar = open("grammar.lark", 'r').read()
code = open("examples/only-expressions.wan", 'r').read()

tree = parseTree(grammar, code)

variables_table = generate_variables_table(tree)
print("Variables table:")
PrettyPrinter().pprint(variables_table)

functions_directory = generate_functions_directory(tree)
PrettyPrinter().pprint(functions_directory)

quadruples = generate_quadruples(tree)
PrettyPrinter().pprint(quadruples)

print(memory)
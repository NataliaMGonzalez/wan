import globals
from lark_parser import parseTree
from pprint import PrettyPrinter
from variables_table import generate_variables_table
from functions_directory import generate_functions_directory
from quadruples import generate_quadruples
from memory_manager import memory

grammar = open("grammar.lark", 'r').read()
code = open("examples/read-write.wan", 'r').read()

tree = parseTree(grammar, code)
# print("Parse Tree:")
# print(tree.pretty())

variables_table = generate_variables_table(tree)
print("\nVariables Table:")
PrettyPrinter().pprint(variables_table)
globals.variables_table = variables_table

functions_directory = generate_functions_directory(tree)
print("\nFunctions Directory:")
PrettyPrinter().pprint(functions_directory)
globals.functions_directory = functions_directory

quadruples = generate_quadruples(tree)
print("\nQuadruples:")
PrettyPrinter().pprint(quadruples)
globals.quadruples = quadruples

# print("\nMemory:")
# PrettyPrinter().pprint(globals.memory)

print("\nConstants:")
PrettyPrinter().pprint(globals.constants)

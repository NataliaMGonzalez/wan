import globals
from lark_parser import parseTree
from pprint import PrettyPrinter
from variables_table import generate_variables_table
from functions_directory import generate_functions_directory
from quadruples import generate_quadruples
import raava

grammar = open("grammar.lark", 'r').read()
code = open("examples/expressions-and-functions.wan", 'r').read()

tree = parseTree(grammar, code)

variables_table = generate_variables_table(tree)
globals.variables_table = variables_table

functions_directory = generate_functions_directory(tree)
globals.functions_directory = functions_directory

quadruples = generate_quadruples(tree)
globals.quadruples = quadruples

# Update the memory with the constant values
memory = globals.memory
for address in globals.constants:
    memory[address] = globals.constants[address]

# print("Parse Tree:")
# print(tree.pretty())

# print("\nVariables Table:")
# PrettyPrinter().pprint(variables_table)

# print("\nFunctions Directory:")
# PrettyPrinter().pprint(functions_directory)

print("\nQuadruples:")
PrettyPrinter().pprint([{num: value} for num, value in enumerate(quadruples)])

# print("\nConstants:")
# PrettyPrinter().pprint(globals.constants)

raava.execute()

# print("\nFinal memory:")
# PrettyPrinter().pprint(globals.memory)

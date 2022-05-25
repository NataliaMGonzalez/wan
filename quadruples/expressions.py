from collections import OrderedDict
from typing import Union
import globals
from lark import Token, Tree
from enums import Operators, ArrayOperations
from addresses_manager import assign_into_extra_segment
from numpy import prod


def get_variable_address(self, variable: Union[Token, Tree]):
    # TODO: Search for memory address of variable and append that address to the stack
    if isinstance(variable, Token):
        variable_name: str = variable.value
        vars_table: OrderedDict = self.get_current_variables_table()
        if variable_name not in vars_table:
            raise Exception("Variable has not been previously declared.")
        return vars_table[variable_name]
    if (variable.data == "self_attribute"):
        return "my:{}".format(variable.children[0].value)
    if (variable.data == "instance_attribute"):
        return "instance_attribute"
    if (variable.data == "function_eval"):
        function_id = variable.children[0].value
        functions_directory = self.get_current_functions_directory()
        function_attributes = functions_directory[function_id]
        return function_attributes["returns"]


def add_expression_quadruple(self, operator):
    right_operand = self.addresses_stack.pop()
    left_operand = self.addresses_stack.pop()
    address = assign_into_extra_segment()
    quad = (operator, left_operand, right_operand, address)
    self.quadruples.append(quad)
    self.addresses_stack.append(address)


def or_expression(self, tree):
    add_expression_quadruple(self, Operators(tree.children[1].value))


def and_expression(self, tree):
    add_expression_quadruple(self, Operators(tree.children[1].value))


def comp_expression(self, tree):
    add_expression_quadruple(self, Operators(tree.children[1].value))


def sum_expression(self, tree):
    add_expression_quadruple(self, Operators(tree.children[1].value))


def term(self, tree):
    add_expression_quadruple(self, Operators(tree.children[1].value))


def numerical_constant(self, tree):
    num_value = tree.children[1].value
    address = assign_into_extra_segment()
    globals.constants[address] = num_value
    self.addresses_stack.append(address)


def bool_constant(self, tree):
    bool_value = tree.children[0].value
    address = assign_into_extra_segment()
    globals.constants[address] = bool_value
    self.addresses_stack.append(address)


def char_constant(self, tree):
    char_value = tree.children[0].value
    address = assign_into_extra_segment()
    globals.constants[address] = char_value
    self.addresses_stack.append(address)


def string_constant(self, tree):
    string_value = tree.children[0].value
    address = assign_into_extra_segment()
    globals.constants[address] = string_value
    self.addresses_stack.append(address)


def assignment_var(self, tree):
    variable = tree.children[0]
    var_name = get_variable_address(self, variable)
    self.addresses_stack.append(var_name)


array_dim = []
array_offsets = []


def var_exp(self, tree):
    if (isinstance(tree, Tree) and isinstance(tree.children[0], Tree) and tree.children[0].data == "arr_exp"):
        return

    variable = tree.children[0]
    var_address = get_variable_address(self, variable)
    self.addresses_stack.append(var_address)


def arr_exp(self, tree: Tree):
    variable, *expressions = tree.children

    exp_addresses = []
    for _ in expressions:
        exp_address = self.addresses_stack.pop()
        exp_addresses = [exp_address] + exp_addresses
    base_address = get_variable_address(self, variable)

    vars_table = self.get_current_variables_table()
    size = vars_table[(variable.value, "size")]

    # Calculate dimensions based on the array sizes
    dims = []
    for idx in range(len(size)):
        dims.append(int(prod(size[idx+1:])))

    total_sum_address = assign_into_extra_segment()
    globals.constants[total_sum_address] = 0
    for exp_address, dim in zip(exp_addresses, dims):
        dim_address = assign_into_extra_segment()
        globals.constants[dim_address] = dim
        mult_address = assign_into_extra_segment()
        quad_multiply = (Operators.MULTIPLY, exp_address,
                         dim_address, mult_address)
        self.quadruples.append(quad_multiply)
        quad_sum = (Operators.ADD, mult_address,
                    total_sum_address, total_sum_address)
        self.quadruples.append(quad_sum)

    result_address = assign_into_extra_segment()
    pointer_quad = (ArrayOperations.POINT_TO, base_address,
                    total_sum_address, result_address)
    self.quadruples.append(pointer_quad)

    self.addresses_stack.append(result_address)

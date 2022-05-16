import globals
from lark import Token
from enums import Operators
from addresses_manager import assign_into_extra_segment


def get_variable_address(self, variable):
    # TODO: Search for memory address of variable and append that address to the stack
    if isinstance(variable, Token):
        variable = variable.value
        variables_table = self.get_current_variables_table()
        address = variables_table[variable]
        return address
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


def var_exp(self, tree):
    variable = tree.children[0]
    var_address = get_variable_address(self, variable)
    self.addresses_stack.append(var_address)

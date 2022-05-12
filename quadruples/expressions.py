from lark import Token
from enums import Operators
from memory_manager import assign_constant
from variables_table import VariablesTable


def get_variable_address(self, variable):
    # TODO: Search for memory address of variable and append that address to the stack
    if isinstance(variable, Token):
        variable = variable.value
        address = VariablesTable.variables_table[variable]
        return address
    if (variable.data == "self_attribute"):
        return "my:{}".format(variable.children[0].value)
    if (variable.data == "instance_attribute"):
        return "instance_attribute"


def add_expression_quadruple(self, operator):
    right_operand = self.addresses_stack.pop()
    left_operand = self.addresses_stack.pop()
    temp_name = "t{}".format(self.temp_count)
    quad = (operator, left_operand, right_operand, temp_name)
    self.quadruples.append(quad)
    self.addresses_stack.append(temp_name)
    self.temp_count += 1


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
    # Exchange token with setting constant in memory and returning its address
    num_const = tree.children[1].value
    address = assign_constant(num_const)
    self.addresses_stack.append(address)


def bool_constant(self, tree):
    # Exchange token with setting constant in memory and returning its address
    num_const = tree.children[0].value
    self.addresses_stack.append(num_const)


def assignment_var(self, tree):
    variable = tree.children[0]
    var_name = get_variable_address(self, variable)
    self.addresses_stack.append(var_name)


def var_exp(self, tree):
    variable = tree.children[0]
    var_address = get_variable_address(self, variable)
    self.addresses_stack.append(var_address)

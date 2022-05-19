from enums import Operators
from addresses_manager import assign_constant, assign_into_extra_segment


def add_operation_quadruple(self, operator):
    right_operand = self.addresses_stack.pop()
    left_operand = self.addresses_stack.pop()
    address = assign_into_extra_segment()
    quad = (operator, left_operand, right_operand, address)
    self.quadruples.append(quad)
    self.addresses_stack.append(address)


def or_expression(self, tree):
    operator = Operators(tree.children[1].value)
    add_operation_quadruple(self, operator)


def and_expression(self, tree):
    operator = Operators(tree.children[1].value)
    add_operation_quadruple(self, operator)


def comp_expression(self, tree):
    operator = Operators(tree.children[1].value)
    add_operation_quadruple(self, operator)


def sum_expression(self, tree):
    operator = Operators(tree.children[1].value)
    add_operation_quadruple(self, operator)


def term(self, tree):
    operator = Operators(tree.children[1].value)
    add_operation_quadruple(self, operator)


def numerical_constant(self, tree):
    is_negative, num = tree.children
    num_value = int(num.value)
    multiplier = -1 if is_negative else 1
    address = assign_constant(num_value * multiplier)
    self.addresses_stack.append(address)


def bool_constant(self, tree):
    bool_value = tree.children[0].value
    address = assign_constant(bool_value)
    self.addresses_stack.append(address)


def char_constant(self, tree):
    char_value = tree.children[0].value
    address = assign_constant(char_value)
    self.addresses_stack.append(address)


def string_constant(self, tree):
    string_value = tree.children[0].value
    address = assign_constant(string_value)
    self.addresses_stack.append(address)

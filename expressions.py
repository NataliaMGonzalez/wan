from lark import v_args
from enums import Operators


def add_expression_quadruple(self, operator):
    right_operand = self.stackAddresses.pop()
    left_operand = self.stackAddresses.pop()
    temp_name = "t{}".format(self.temp_count)
    quad = (operator, left_operand, right_operand, temp_name)
    self.quadruples.append(quad)
    self.stackAddresses.append(temp_name)
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
    num_const = tree.children[1].value
    self.stackAddresses.append(num_const)

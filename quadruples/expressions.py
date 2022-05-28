from collections import OrderedDict
from typing import Union
from lark import Token, Tree
from enums import Operators, ArrayOperations
from addresses_manager import assign_constant, assign_into_extra_segment
from numpy import prod


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
    address = assign_constant(num_value)
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

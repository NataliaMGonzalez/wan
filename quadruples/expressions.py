from lark import Tree
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


def not_expression(self, _tree: Tree):
    operand = self.addresses_stack.pop()
    address = assign_into_extra_segment()
    quad = (Operators.NOT, operand, address)
    self.quadruples.append(quad)
    self.addresses_stack.append(address)


def comp_expression(self, tree):
    operator = Operators(tree.children[1].value)
    add_operation_quadruple(self, operator)


def sum_expression(self, tree):
    operator = Operators(tree.children[1].value)
    add_operation_quadruple(self, operator)


def term(self, tree):
    operator = Operators(tree.children[1].value)
    add_operation_quadruple(self, operator)

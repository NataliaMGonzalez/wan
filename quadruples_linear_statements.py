from enums import Operators
from lark.visitors import Visitor_Recursive


def generate_quadruples(tree):
    Quadruples().visit(tree)
    return Quadruples.quadruples


class Quadruples(Visitor_Recursive):
    quadruples = []
    stackAddresses = []
    temp_count = 1

    def add_quadruple(self, tree):
        right_operand = self.stackAddresses.pop()
        left_operand = self.stackAddresses.pop()
        operator = Operators(tree.children[1].value)
        temp_name = "t{}".format(self.temp_count)
        quad = [operator, left_operand, right_operand, temp_name]
        self.quadruples.append(quad)
        self.stackAddresses.append(temp_name)
        self.temp_count += 1

    def or_expression(self, tree):
        self.add_quadruple(tree)

    def and_expression(self, tree):
        self.add_quadruple(tree)

    def comp_expression(self, tree):
        self.add_quadruple(tree)

    def sum_expression(self, tree):
        self.add_quadruple(tree)

    def term(self, tree):
        self.add_quadruple(tree)

    def numerical_constant(self, tree):
        num_const = tree.children[1].value
        self.stackAddresses.append(num_const)

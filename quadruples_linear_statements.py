from enums import Operators
from lark import Visitor


def generate_quadruples(tree):
    Quadruples().visit_topdown(tree)
    return Quadruples.quadruples


class Quadruples(Visitor):
    quadruples = []
    stackAddresses = []
    stackOperators = []
    temp_count = 1

    def expression(self, tree):
        print(tree.pretty())

    def np_add_quadruple(self, _tree):
        right_operand = self.stackAddresses.pop()
        left_operand = self.stackAddresses.pop()
        operator = self.stackOperators.pop()
        temp_name = "t{}".format(self.temp_count)
        quad = [operator, left_operand, right_operand, temp_name]
        self.quadruples.append(quad)
        self.stackAddresses.append(temp_name)
        self.temp_count += 1

    def np_add_assignment_quadruple(self, _tree):
        right_operand = self.stackAddresses.pop()
        left_operand = self.stackAddresses.pop()
        operator = self.stackOperators.pop()
        quad = [operator, left_operand, right_operand]
        self.quadruples.append(quad)

    def assignment_operator(self, tree):
        self.stackOperators.append(tree.children[0].value)

    def or_expression_operator(self, tree):
        self.stackOperators.append(tree.children[0].value)

    def and_expression_operator(self, tree):
        self.stackOperators.append(tree.children[0].value)

    def relop(self, tree):
        self.stackOperators.append(tree.children[0].value)

    def sum_expression_operator(self, tree):
        self.stackOperators.append(tree.children[0].value)

    def term_operator(self, tree):
        self.stackOperators.append(tree.children[0].value)

    def assignment_var(self, tree):
        # Search for memory address of var and append the address
        self.stackAddresses.append(tree.children[0].value)

    def numerical_constant(self, tree):
        # Add numerical constant to memory and append the address
        num_const = tree.children[1].value
        self.stackAddresses.append(num_const)

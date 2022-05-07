from enums import Operators
from lark import Visitor


def generate_quadruples(tree):
    Quadruples().visit_topdown(tree)
    return Quadruples.quadruples

class Quadruples(Visitor):
    quadruples = []
    temp_count = 1
    stackAddresses = []
    stackOperators = []
    latest = []

    def expression(self, tree):
        print(tree.pretty())

    # def np_pop_oper(self, tree):
    #     self.isTopOperator()

    # def isTopOperator(self):
    #     top = self.stackOperators[-1]
    #     if(top in Operators._value2member_map_):
    #         print("is top operator true")
    #         print(self.stackOperators)
    #         return True

    def add_quadruple(self, _tree):
        right_operand = self.stackAddresses.pop()
        left_operand = self.stackAddresses.pop()
        operator = self.stackOperators.pop()
        temp_name = "t{}".format(self.temp_count)
        quad = [operator, left_operand, right_operand, temp_name]
        self.quadruples.append(quad)
        self.stackAddresses.append(temp_name)
        self.temp_count += 1

    def sum_expression_operator(self, tree):
        self.stackOperators.append(tree.children[0].value)

    def term_operator(self, tree):
        self.stackOperators.append(tree.children[0].value)

    def numerical_constant(self, tree):
        num_const = tree.children[1].value
        print("numerical constant: ", num_const)
        self.stackAddresses.append(num_const)

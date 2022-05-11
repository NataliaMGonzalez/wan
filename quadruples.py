from lark.visitors import Visitor_Recursive


def generate_quadruples(tree):
    Quadruples().visit(tree)
    return Quadruples.quadruples


class Quadruples(Visitor_Recursive):
    from expressions import (or_expression, and_expression,
                             comp_expression, sum_expression, term, numerical_constant)

    quadruples = []
    stackAddresses = []
    temp_count = 1

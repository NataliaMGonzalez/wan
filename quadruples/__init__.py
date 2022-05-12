from lark.visitors import Visitor_Recursive


def generate_quadruples(tree):
    Quadruples().visit(tree)
    return Quadruples.quadruples


class Quadruples(Visitor_Recursive):
    from quadruples.expressions import (or_expression, and_expression, comp_expression,
                                        sum_expression, term, numerical_constant, assignment_var, var_exp)
    from quadruples.assignments import assignment

    quadruples = []
    addresses_stack = []
    temp_count = 1  # To be deleted after implementing memory

from lark.visitors import Visitor_Recursive


def generate_quadruples(tree):
    Quadruples().visit(tree)
    return Quadruples.quadruples


class Quadruples(Visitor_Recursive):
<<<<<<< HEAD:quadruples/__init__.py
    from quadruples.expressions import (or_expression, and_expression, comp_expression,
                                        sum_expression, term, numerical_constant, assignment_var, var_exp)
    from quadruples.assignments import assignment
=======
    from expressions import (or_expression, and_expression, comp_expression,
                             sum_expression, term, numerical_constant, assignment_var, var_exp)
    from assignments import assignment
    from conditionals import np_conditional_gotof, np_conditional_else, conditional
>>>>>>> b08aebb (quadruples for conditional statements):quadruples.py

    quadruples = []
    addresses_stack = []
    jump_stack = []
    temp_count = 1  # To be deleted after implementing memory

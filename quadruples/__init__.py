from enums import FunctionOperators
import globals
from lark import Tree
from lark.visitors import Visitor_Recursive
from quadruples.declaration_jump import (
    create_declaration_jump, restore_declaration_jump)


def generate_quadruples(tree):
    Quadruples().visit(tree)
    return Quadruples.quadruples


class Quadruples(Visitor_Recursive):
    from quadruples.expressions import (
        or_expression, and_expression, comp_expression, sum_expression, term,
        numerical_constant, bool_constant, char_constant, string_constant)
    from quadruples.assignments import assignment
    from quadruples.conditionals import (
        np_conditional_gotof, np_conditional_else, conditional)
    from quadruples.cycles import np_cycle_start, np_cycle_gotof, np_cycle_end
    from quadruples.input_output import np_write, read
    from quadruples.functions import function_eval, return_statement
    from quadruples.var_exp import (
        var_exp, np_set_class_function, np_clear_class_function)

    class_context = None
    function_context = None
    quadruples = []
    addresses_stack = []
    jump_stack = []

    declaration_jump = None

    def get_current_variables_table(self, closed_scope=False):
        table = globals.variables_table
        if self.class_context is not None:
            if closed_scope:
                table = table[self.class_context]
            else:
                table = {**table, **table[self.class_context]}
        if self.function_context is not None:
            if closed_scope:
                table = table[self.function_context]
            else:
                table = {**table, **table[self.function_context]}
        return table

    def get_current_functions_directory(self, closed_scope=False):
        directory = globals.functions_directory
        if self.class_context is not None:
            if closed_scope:
                directory = {**directory, **directory[self.class_context]}
            else:
                directory = directory[self.class_context]
        return directory

    def class_id(self, tree: Tree):
        self.declaration_jump = create_declaration_jump(self)
        class_id = tree.children[0].value
        self.class_context = class_id

    def class_declaration(self, _tree: Tree):
        restore_declaration_jump(self)
        self.class_context = None

    def function_id(self, tree: Tree):
        # Declare jump to not execute on first load
        if self.declaration_jump is None:
            self.declaration_jump = create_declaration_jump(self)
        function_id: str = tree.children[0].value
        directory = self.get_current_functions_directory()
        directory[function_id]["position"] = len(self.quadruples)
        self.function_context = function_id

    def function_declaration(self, _tree: Tree):
        end_quadruple = (FunctionOperators.RETURN,)
        self.quadruples.append(end_quadruple)
        restore_declaration_jump(self)
        self.function_context = None

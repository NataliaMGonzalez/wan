from typing import List
from enums import FunctionOperators


def set_function_remaining(self, function_id: str):
    """Save quadruples generation for later when reading a not yet declared function.

    When referencing a function whose instruction pointer position still don't
    know, save it into the remaining functions to later update it.
    """
    remaining_functions = self.remaining_functions
    current_class = self.class_context

    # Add the current instruction line into the pending quadruples for later
    go_sub_line = len(self.quadruples)
    if current_class:
        if current_class not in remaining_functions:
            remaining_functions[current_class] = {}
        remaining_functions = remaining_functions[current_class]
    if function_id not in remaining_functions:
        remaining_functions[function_id] = []
    remaining_functions[function_id].append(go_sub_line)


def retreive_remaining_function(self, function_id, function_position):
    """Complete function quadruple when declaring the required function.

    On function declaration, when discovering its start position, update it in
    all of the quadruples where it was unknown.
    """
    remaining_functions = self.remaining_functions
    current_class: str = self.class_context

    # Retrieve the pending quadruples lines
    quadruple_lines = []
    if current_class and current_class in remaining_functions:
        remaining_functions = remaining_functions[current_class]
    if function_id in remaining_functions:
        quadruple_lines: List[int] = remaining_functions[function_id]

    # Update the quadruple at the required lines
    for line in quadruple_lines:
        new_quadruple = (FunctionOperators.GOSUB, function_position)
        self.quadruples[line] = new_quadruple

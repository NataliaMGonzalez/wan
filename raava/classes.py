import globals
from typing import Tuple
from enums import ClassOperations
from raava import common


def execute_class_operation(quadruple: Tuple[ClassOperations, int]):
    instruction = quadruple[0]
    if instruction == ClassOperations.SET_FUNCTION_CLASS:
        new_class = quadruple[1]
        if new_class != ClassOperations.SELF_ATTRIBUTE:
            common.current_class = quadruple[1]
    if instruction == ClassOperations.CLEAR_FUNCTION_CLASS:
        common.current_class = None

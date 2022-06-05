from globals import class_variables, memory
from typing import Tuple
from enums import ClassOperations
from raava import common
from raava.memory import get_address


def execute_class_operation(quadruple: Tuple[ClassOperations, int]):
    instruction = quadruple[0]
    if instruction == ClassOperations.SELF_ATTRIBUTE:
        _, attribute, pointer_address = quadruple
        class_address = get_address(common.current_class)
        target_address = class_variables[class_address][attribute]
        memory[pointer_address] = (target_address,)
    if instruction == ClassOperations.INSTANCE_ATTRIBUTE:
        _, class_address, attribute, pointer_address = quadruple
        class_address = get_address(class_address)
        target_address = class_variables[class_address][attribute]
        memory[pointer_address] = (target_address,)
    if instruction == ClassOperations.SET_FUNCTION_CLASS:
        new_class = quadruple[1]
        if new_class != ClassOperations.SELF_ATTRIBUTE:
            common.current_class = quadruple[1]
    if instruction == ClassOperations.CLEAR_FUNCTION_CLASS:
        common.current_class = None

from globals import class_variables, memory
from typing import Tuple
from enums import ClassOperations
from raava import common
from raava.memory import get_address


def execute_class_operation(quadruple: Tuple[ClassOperations, ...]):
    """Execute the different class operations."""
    instruction = quadruple[0]
    if instruction == ClassOperations.SELF_ATTRIBUTE:
        execute_self_attribute(quadruple)
    if instruction == ClassOperations.INSTANCE_ATTRIBUTE:
        execute_instance_attribute(quadruple)
    if instruction == ClassOperations.SET_FUNCTION_CLASS:
        set_function_class(quadruple)
    if instruction == ClassOperations.CLEAR_FUNCTION_CLASS:
        clear_function_class(quadruple)


def execute_self_attribute(quadruple: Tuple[ClassOperations, str, int]):
    """Create a pointer to the requested address of the current instance."""
    _, attribute, pointer_address = quadruple
    class_address = get_address(common.current_class)
    target_address = class_variables[class_address][attribute]
    memory[pointer_address] = (target_address,)


def execute_instance_attribute(
        quadruple: Tuple[ClassOperations, int, str, int]):
    """Create a pointer to the requested address of the given instance."""
    _, class_address, attribute, pointer_address = quadruple
    class_address = get_address(class_address)
    target_address = class_variables[class_address][attribute]
    memory[pointer_address] = (target_address,)


def set_function_class(quadruple: Tuple[ClassOperations, int]):
    """Execute the quadruple for setting the class context within a function.

    Before starting an instance or a self function, set the class context to the
    given instance.
    """
    instance_address = quadruple[1]
    if instance_address != ClassOperations.SELF_ATTRIBUTE:
        common.current_class = quadruple[1]


def clear_function_class(_quadruple: Tuple[ClassOperations]):
    """Execute the quadruple for clearing the instance context after a function.

    After executing the function, clear the instance context set in `set_function_class`.
    """
    common.current_class = None

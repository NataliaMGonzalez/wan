import raava.common


def execute_goto(quadruple):
    """Updates the instruction pointer to the desired new instruction."""
    new_instruction = quadruple[1]
    raava.common.instruction_pointer = new_instruction - 1

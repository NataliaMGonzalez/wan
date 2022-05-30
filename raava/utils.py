import raava.common


def execute_goto(quadruple):
    new_instruction = quadruple[1]
    raava.common.instruction_pointer = new_instruction - 1

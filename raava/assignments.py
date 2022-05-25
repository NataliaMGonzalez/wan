import globals


memory = globals.memory


def execute_assignment(quadruple):
    _, new_address, original_address, temp_address = quadruple
    memory[new_address] = memory[temp_address] = memory[original_address]

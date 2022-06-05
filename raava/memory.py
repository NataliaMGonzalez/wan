import globals


def get_address(address) -> int:
    """ Traverse the pointers until finding a direct value. """
    memory = globals.memory
    if address not in memory:
        return address
    value = memory[address]
    if not isinstance(memory[address], tuple):
        return address
    return get_address(value[0])

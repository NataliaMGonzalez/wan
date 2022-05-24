from enums import InputOutputInstructions
from memory_manager import assign_into_extra_segment


def np_write(self, _tree):
    output = self.addresses_stack.pop()
    quad = (InputOutputInstructions.WRITE, output)
    self.quadruples.append(quad)


def read(self, _tree):
    address = assign_into_extra_segment(None)
    quad = (InputOutputInstructions.READ, address)
    self.quadruples.append(quad)
    self.addresses_stack.append(address)

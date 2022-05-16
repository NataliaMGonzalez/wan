from enums import Operators
from memory_manager import assign_into_extra_segment



def assignment(self, _tree):
    operand = self.addresses_stack.pop()
    var_name = self.addresses_stack.pop()
    address = assign_into_extra_segment(None)
    quad = (Operators.ASSIGN, var_name, operand, address)
    self.quadruples.append(quad)
    self.addresses_stack.append(address)
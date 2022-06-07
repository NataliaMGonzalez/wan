from lark import Tree
from enums import InputOutputInstructions
from addresses_manager import assign_into_extra_segment


def np_write(self, _tree: Tree):
    """Create the quadruples for printing an expression.

    Retreive the last expression address and create a quadruple with a write
    operation and the last expression.
    This neuralgic point will be executed for each of the expressions in the
    comma separated list inside the `print()` expression.
    """
    output = self.addresses_stack.pop()
    quad = (InputOutputInstructions.WRITE, output)
    self.quadruples.append(quad)


def read(self, _tree: Tree):
    """Create the quadruples for getting an input.

    In the virtual machine this quadruple will request for the user to introduce
    a value. The resulting input will be saved into an address which can be used
    in other expressions and operations.
    """
    address = assign_into_extra_segment()
    quad = (InputOutputInstructions.READ, address)
    self.quadruples.append(quad)
    self.addresses_stack.append(address)

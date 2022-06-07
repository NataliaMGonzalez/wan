from lark import Tree
from enums import InstructionPointerJump


def add_current_to_jump_stack(self):
    """Add the current position into the jump stack for later retreival."""
    pointer = len(self.quadruples)
    self.jump_stack.append(pointer)


def np_cycle_start(self, _tree: Tree):
    """When starting the cycle, add the current position into the jump stack."""
    add_current_to_jump_stack(self)


def np_cycle_gotof(self, _tree: Tree):
    """Create and add to the list the GOTO_FALSE quadruple.

    When finishing reading the expression, append quadruple to indicate gotoF
    operation in case the expression is False. This will break out of the while
    loop once the condition is false.
    """
    temp = self.addresses_stack.pop()
    quad = (InstructionPointerJump.GOTOF, temp, '')
    add_current_to_jump_stack(self)
    self.quadruples.append(quad)


def np_cycle_end(self, _tree: Tree):
    """Complete gotoF quadruple.

    When finishing the cycle, get the pending incomplete quadruple appended at
    the beginning, and complete it by setting the current instruction as the
    jump address.
    """
    while_gotof = self.jump_stack.pop()
    incomplete_quad = list(self.quadruples[while_gotof])
    incomplete_quad[-1] = len(self.quadruples) + 1
    complete_quad = tuple(incomplete_quad)
    self.quadruples[while_gotof] = complete_quad

    # At the end of the cycle, add the quadruple to return to the beginning.
    while_start = self.jump_stack.pop()
    quad = (InstructionPointerJump.GOTO, while_start)
    self.quadruples.append(quad)

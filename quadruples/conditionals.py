from lark import Tree
from enums import InstructionPointerJump


def complete_quad(self):
    """Complete the last incomplete quadruple."""
    pending_jump_instruction = self.jump_stack.pop()
    incomplete_quad = list(self.quadruples[pending_jump_instruction])
    jump_instruction = len(self.quadruples)
    incomplete_quad[-1] = jump_instruction
    complete_quad = tuple(incomplete_quad)
    self.quadruples[pending_jump_instruction] = complete_quad


def add_current_to_jump_stack(self):
    """Add current position into the jump stack for later retreival."""
    pointer = len(self.quadruples) - 1
    self.jump_stack.append(pointer)


def np_conditional_gotof(self, _tree: Tree):
    """Create and append gotoF instruction pointer.

    Will remain incomplete until `complete_quad` is called.
    """
    temp = self.addresses_stack.pop()
    quad = (InstructionPointerJump.GOTOF, temp, '')
    self.quadruples.append(quad)
    add_current_to_jump_stack(self)


def np_conditional_else(self, _tree: Tree):
    """Complete last pending quadruple (from conditional start).

    Create and append goto instruction quadruple. Will remain incomplete until
    `complete_quad` is called.
    """
    quad = (InstructionPointerJump.GOTO, '')
    self.quadruples.append(quad)
    complete_quad(self)
    add_current_to_jump_stack(self)


def conditional(self, _tree: Tree):
    """When finishing reading the conditional, complete the last pending quadruple."""
    complete_quad(self)

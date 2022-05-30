from lark import Token
from enums import InstructionPointerJump


def complete_quad(self):
    # complete last incomplete quad
    pointer = self.jump_stack.pop()
    incomplete_quad = list(self.quadruples[pointer])
    incomplete_quad[-1] = len(self.quadruples)
    complete_quad = tuple(incomplete_quad)
    self.quadruples[pointer] = complete_quad


def add_current_to_jump_stack(self):
    # add current position to jump stack
    pointer = len(self.quadruples) - 1
    self.jump_stack.append(pointer)


def np_conditional_gotof(self, tree):
    temp = self.addresses_stack.pop()
    quad = (InstructionPointerJump.GOTOF, temp, '')
    self.quadruples.append(quad)
    add_current_to_jump_stack(self)


def np_conditional_else(self, tree):
    quad = (InstructionPointerJump.GOTO, '')
    self.quadruples.append(quad)
    complete_quad(self)
    add_current_to_jump_stack(self)


def conditional(self, tree):
    complete_quad(self)

from enums import InstructionPointerJump


def add_current_to_jump_stack(self):
    # add current position to jump stack
    pointer = len(self.quadruples)
    self.jump_stack.append(pointer)


def np_cycle_start(self, tree):
    add_current_to_jump_stack(self)


def np_cycle_gotof(self, tree):
    temp = self.addresses_stack.pop()
    quad = (InstructionPointerJump.GOTOF, temp, '')
    add_current_to_jump_stack(self)
    self.quadruples.append(quad)


def np_cycle_end(self, tree):
    print(self.jump_stack)
    # complet gotoF quadruple
    while_gotof = self.jump_stack.pop()
    incomplete_quad = list(self.quadruples[while_gotof])
    incomplete_quad[-1] = len(self.quadruples) + 1
    complete_quad = tuple(incomplete_quad)
    print(complete_quad)
    self.quadruples[while_gotof] = complete_quad

    # return to while start
    while_start = self.jump_stack.pop()
    quad = (InstructionPointerJump.GOTO, while_start)
    self.quadruples.append(quad)

from enums import InstructionPointerJump


def create_declaration_jump(self):
    self.quadruples.append((InstructionPointerJump.GOTO, None))
    return len(self.quadruples) - 1


def restore_declaration_jump(self):
    if self.declaration_jump is not None:
        declaration_start = self.declaration_jump
        self.quadruples[declaration_start] = (
            InstructionPointerJump.GOTO, len(self.quadruples))
        self.declaration_jump = None

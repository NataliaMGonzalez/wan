from enums import InstructionPointerJump


def create_declaration_jump(self):
    """Create jump quadruple to avoid executing the contents of inside declarations.

    Add quadruples to jump the declarations to avoid executing the contents of
    the functions unless they are explicitly called. Quadruple will remain
    incomplete until the `restore_declaration_jump` function is executed.
    """
    self.quadruples.append((InstructionPointerJump.GOTO, None))
    return len(self.quadruples) - 1


def restore_declaration_jump(self):
    """Complete the pending jump at the end of the declaration.

    At the end of the declaration, retreive the pending jump quadruple created
    in the `create_declaration_jump` function and complete it with the current
    instruction.
    """
    if self.declaration_jump is not None:
        declaration_start = self.declaration_jump
        self.quadruples[declaration_start] = (
            InstructionPointerJump.GOTO, len(self.quadruples))
        self.declaration_jump = None

from memory_manager import assign_into_extra_segment


def np_write(self, tree):
    output = self.addresses_stack.pop()
    quad = ("PRINT", output)
    self.quadruples.append(quad)


def read(self, tree):
    address = assign_into_extra_segment(None)
    quad = ("READ", address)
    self.quadruples.append(quad)

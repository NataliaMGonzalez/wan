from enums import Operators


def assignment(self, _tree):
    operand = self.addresses_stack.pop()
    var_name = self.addresses_stack.pop()
    temp_name = "t{}".format(self.temp_count)
    quad = (Operators.ASSIGN, var_name, operand, temp_name)
    self.quadruples.append(quad)
    self.addresses_stack.append(temp_name)
    self.temp_count += 1

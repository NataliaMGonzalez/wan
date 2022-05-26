from lark import Tree
from enums import AssignmentOperators
from addresses_manager import assign_into_extra_segment


def assignment(self, _tree: Tree):
    assignor: int = self.addresses_stack.pop()
    asignee: int = self.addresses_stack.pop()
    exp_address: int = assign_into_extra_segment()
    quad = (AssignmentOperators.ASSIGN, asignee, assignor, exp_address)
    self.quadruples.append(quad)
    self.addresses_stack.append(exp_address)

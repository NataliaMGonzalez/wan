from lark import Tree
from enums import AssignmentOperators


def assignment(self, _tree: Tree):
    assignor: int = self.addresses_stack.pop()
    asignee: int = self.addresses_stack.pop()
    quad = (AssignmentOperators.ASSIGN, asignee, assignor)
    self.quadruples.append(quad)

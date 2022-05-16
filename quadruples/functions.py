from collections import OrderedDict
from lark import Tree
from enums import FunctionOperators, Operators


def function_eval(self, tree: Tree):
    id_token, *argument_tokens = tree.children
    id: str = id_token.value
    func_directory: OrderedDict = self.get_current_functions_directory()
    vars_table: OrderedDict = self.get_current_variables_table(
        closed_scope=True)
    vars_addresses: list[int] = list(vars_table.values())
    function_attributes: OrderedDict = func_directory[id]

    # Check for argument - parameters mismatch
    func_parameters = function_attributes["parameters"]
    if len(argument_tokens) != len(func_parameters):
        raise Exception(
            "The number of arguments does not match for function {}.".format(
                id))

    # Save all of the current variables in a stack to for later restoration
    if self.function_context != None:
        for address in vars_addresses:
            save_state_quadruple = (FunctionOperators.PUSH_IN_STACK, address)
            self.quadruples.append(save_state_quadruple)

    # Update parameters with the arguments' values
    for parameter in func_parameters:
        argument_address = self.addresses_stack.pop()
        assignment_quadruple = (
            Operators.ASSIGN, parameter, argument_address)
        self.quadruples.append(assignment_quadruple)

    # Go into function
    function_position = function_attributes["position"]
    go_to_quadruple = (FunctionOperators.GOSUB, function_position)
    self.quadruples.append(go_to_quadruple)

    # When returning, retrive the stored variables to restore the state
    if self.function_context != None:
        for address in vars_addresses[::-1]:
            retreival_quadruple = (FunctionOperators.PULL_FROM_STACK, address)
            self.quadruples.append(retreival_quadruple)


def return_statement(self, _tree: Tree):
    func_directory: OrderedDict = self.get_current_functions_directory()
    return_address: int = func_directory[self.function_context]["returns"]
    return_expression: int = self.addresses_stack.pop()
    assignment_quadruple = (
        Operators.ASSIGN, return_address, return_expression)
    self.quadruples.append(assignment_quadruple)
    end_quadruple = (FunctionOperators.END_FUNC)
    self.quadruples.append(end_quadruple)

from lark import Tree
from enums import FunctionOperators, Operators


def function_eval(self, tree: Tree):
    id_token, *argument_tokens = tree.children
    id = id_token.value
    func_directory = self.get_current_functions_directory()
    vars_table = self.get_current_variables_table(closed_scope=True)
    vars_addresses = list(vars_table.values())
    function_attributes = func_directory[id]
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

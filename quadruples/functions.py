from collections import OrderedDict
from lark import Tree
from addresses_manager import get_type_by_address
from variables_table import get_variable_size
from enums import FunctionOperators
from quadruples.remaining_functions import set_function_remaining


def function_eval(self, tree: Tree):
    """Create all of the quadruples required on function evaluation.

    On function evaluation, create all of the quadruples for setting the parameters,
    creating the memory copy, calling the function, returning from the function
    and restoring the memory.
    """
    id_token, *argument_tokens = tree.children
    id: str = id_token.value
    vars_table: OrderedDict = self.current_variables_table

    # Get and filter the vars addresses
    vars_addresses: list[int] = list(vars_table.values())
    def is_not_array(a): return not isinstance(a, list)
    vars_addresses: list[int] = list(filter(is_not_array, vars_addresses))

    func_directory: OrderedDict = self.functions_directory
    function_attributes = None
    if len(self.classes_stack) > 0:
        class_type = self.classes_stack.pop()
        if class_type != self.class_context:
            func_directory = func_directory[class_type]

    function_attributes: OrderedDict = func_directory[id]

    # Check for argument - parameters mismatch
    func_parameters = function_attributes["parameters"]
    if len(argument_tokens) != len(func_parameters):
        raise Exception(
            "The number of arguments does not match for function {}.".format(
                id))

    # To restore the value of the temporals after returning from function
    temporals_saved = self.addresses_stack.copy()

    # Save all of the current variables in a stack to for later restoration
    if self.function_context != None:
        for address in vars_addresses:
            push_in_stack(self, vars_table, address)
        for addresses in temporals_saved:
            save_state_quadruple = (FunctionOperators.PUSH_IN_STACK, addresses)
            self.quadruples.append(save_state_quadruple)

    # Update parameters with the arguments' values
    for parameter in func_parameters:
        parameter_attributes = func_parameters[parameter]
        save_param(self, parameter_attributes)

    # Go into function
    function_position = function_attributes["position"]
    if function_position is None:
        set_function_remaining(self, id)
    go_to_quadruple = (FunctionOperators.GOSUB, function_position)
    self.quadruples.append(go_to_quadruple)

    # When returning, retrive the stored variables to restore the state
    if self.function_context != None:
        for address in temporals_saved[::-1]:
            save_state_quadruple = (
                FunctionOperators.PULL_FROM_STACK, address)
            self.quadruples.append(save_state_quadruple)
        for address in vars_addresses[::-1]:
            size = get_variable_size(vars_table, address)
            for i in range(size):
                address_index = address + size - i - 1
                retreival_quadruple = (
                    FunctionOperators.PULL_FROM_STACK, address_index)
                self.quadruples.append(retreival_quadruple)


def push_in_stack(self, vars_table: OrderedDict, address: int):
    """Create the quadruple for pushing a specific address into the function stack."""
    size = get_variable_size(vars_table, address)
    for i in range(size):
        save_state_quadruple = (
            FunctionOperators.PUSH_IN_STACK, address + i)
        self.quadruples.append(save_state_quadruple)


def save_param(self, parameter_attributes: OrderedDict):
    """Creates the save param quadruple.

    Raises an error if there is a type mismatch between the parameter and the
    argument to save.
    """
    argument_address = self.addresses_stack.pop()
    argument_type = get_type_by_address(argument_address)
    size = parameter_attributes["size"]
    parameter_address = parameter_attributes["address"]
    assignment_quadruple = (
        FunctionOperators.SAVE_PARAM, parameter_address, argument_address)
    self.quadruples.append(assignment_quadruple)


def return_statement(self, _tree: Tree):
    """Create the quadruples for returning a value from a function.

    Set the value of the expression into the function return specified address,
    update it and move to the last instruction pointer before entering the function.
    """
    func_directory: OrderedDict = self.functions_directory
    function_attributes = func_directory[self.function_context]
    end_quadruple = (FunctionOperators.RETURN,)
    if "returns" in function_attributes:
        return_address: int = function_attributes["returns"]
        return_expression: int = self.addresses_stack.pop()
        end_quadruple = (FunctionOperators.RETURN,
                         return_address, return_expression)
    self.quadruples.append(end_quadruple)

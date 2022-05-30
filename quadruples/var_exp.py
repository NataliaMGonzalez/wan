from collections import OrderedDict
from typing import Union
from lark import Token, Tree
from numpy import prod
from addresses_manager import assign_constant, assign_into_extra_segment
from enums import ArrayOperations, Operators


def assignment_var(self, tree):
    variable = tree.children[0]
    var_name = get_variable_address(self, variable)
    self.addresses_stack.append(var_name)


def var_exp(self, tree):
    variable = tree.children[0]
    var_address = get_variable_address(self, variable)
    self.addresses_stack.append(var_address)


def get_variable_address(self, variable: Union[Token, Tree]):
    """ Based on a variable token or tree, get the variable address. """
    if isinstance(variable, Token):
        variable_name: str = variable.value
        vars_table: OrderedDict = self.get_current_variables_table()
        if variable_name not in vars_table:
            raise Exception("Variable has not been previously declared.")
        return vars_table[variable_name]
    if (variable.data == "arr_exp"):
        return get_arr_exp(self, variable)
    if (variable.data == "self_attribute"):
        return "my:{}".format(variable.children[0].value)
    if (variable.data == "instance_attribute"):
        return "instance_attribute"
    if (variable.data == "function_eval"):
        function_id = variable.children[0].value
        functions_directory = self.get_current_functions_directory()
        function_attributes = functions_directory[function_id]
        return function_attributes["returns"]
    if (variable.data == "var_exp"):
        return get_variable_address(self, variable.children[0])


def get_arr_exp(self, tree: Tree) -> int:
    """ Create quadruples to access exact address in array. """
    variable, *expressions = tree.children

    exp_addresses = []
    for _ in expressions:
        exp_address = self.addresses_stack.pop()
        exp_addresses = [exp_address] + exp_addresses
    base_address = get_variable_address(self, variable)

    vars_table = self.get_current_variables_table()
    size = vars_table[(base_address, "size")]

    # Calculate dimensions based on the array sizes
    dims = []
    for idx in range(len(size)):
        dims.append(int(prod(size[idx+1:])))

    total_sum_address = assign_constant(0)
    for exp_address, dim in zip(exp_addresses, dims):
        dim_address = assign_constant(dim)
        mult_address = assign_into_extra_segment()
        quad_multiply = (Operators.MULTIPLY, exp_address,
                         dim_address, mult_address)
        self.quadruples.append(quad_multiply)
        quad_sum = (Operators.ADD, mult_address,
                    total_sum_address, total_sum_address)
        self.quadruples.append(quad_sum)

    result_address = assign_into_extra_segment()
    pointer_quad = (ArrayOperations.POINT_TO, base_address,
                    total_sum_address, result_address)
    self.quadruples.append(pointer_quad)

    return result_address

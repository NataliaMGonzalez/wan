from lark import Tree
from numpy import prod
import globals
from lark.visitors import Visitor_Recursive
from enums import DataTypes
from addresses_manager import assign_primitive_to_memory


def generate_functions_directory(tree):
    FunctionsDirectory().visit(tree)
    return FunctionsDirectory.functions_directory


class FunctionsDirectory(Visitor_Recursive):
    class_context = None
    functions_directory = {}

    @property
    def current_directory(self):
        """Functions directory available from the current and only the current scope."""
        directory = self.functions_directory
        if self.class_context is not None:
            directory = directory[self.class_context]
        return directory

    @property
    def current_table(self):
        """Variables available from the current and only the current scope."""
        table = globals.variables_table
        if self.class_context is not None:
            table = table[self.class_context]
        return table

    def class_id(self, tree):
        class_id = tree.children[0].value
        self.current_directory[class_id] = {}
        self.class_context = class_id

    def class_declaration(self, _tree):
        self.class_context = None

    def function_declaration(self, tree):
        return_token, id, *parameters, _body = tree.children
        function_id = id.children[0].value
        directory = self.current_directory

        # Check if the function has already been declared
        if function_id in directory:
            raise TypeError(
                "Function \"{}\" already declared in this scope.".format(
                    function_id))

        # Creating the parameters objects
        parameter_entries = {}
        for parameter in parameters:
            self.insert_in_parameter_entry(
                parameter_entries, function_id, parameter)

        # Specifying the return address
        return_type = None
        if return_token.value != "action":
            return_type = DataTypes(return_token.value)
        return_address = None
        if return_type is not None:
            return_address = assign_primitive_to_memory(return_type)

        table_entry = {
            "returns": return_address,
            "parameters": parameter_entries,
            "position": None,
        }
        directory[function_id] = table_entry

    def insert_in_parameter_entry(
            self, parameter_entries: dict, function_id: str, parameter: Tree):
        _, name, *sizes = parameter.children
        function_variables = self.current_table[function_id]
        name = name.value
        total_size = int(prod(sizes))
        address = function_variables[name]
        parameter_entries[name] = {"address": address, "size": total_size}

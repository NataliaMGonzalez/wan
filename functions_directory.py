import globals
from pyclbr import Function
from lark.visitors import Visitor_Recursive
from enums import DataTypes, FunctionReturnTypes
from addresses_manager import assign_to_memory


def generate_functions_directory(tree):
    FunctionsDirectory().visit(tree)
    return FunctionsDirectory.functions_directory


class FunctionsDirectory(Visitor_Recursive):
    class_context = None
    functions_directory = {}

    def get_current_directory(self):
        directory = self.functions_directory
        if self.class_context is not None:
            directory = directory[self.class_context]
        return directory

    def get_current_table(self):
        table = globals.variables_table
        if self.class_context is not None:
            table = table[self.class_context]
        return table

    def class_id(self, tree):
        class_id = tree.children[0].value
        self.get_current_directory()[class_id] = {}
        self.class_context = class_id

    def class_declaration(self, _tree):
        self.class_context = None

    def function_declaration(self, tree):
        return_token, id, *parameters, _body = tree.children
        function_id = id.children[0].value
        directory = self.get_current_directory()
        if function_id in directory:
            raise TypeError(
                "Function \"{}\" already declared in this scope.".format(
                    function_id))
        return_type = None
        if return_token.value != "action":
            return_type = DataTypes(return_token.value)
        function_variables = self.get_current_table()[function_id]
        parameter_names = list(
            map(lambda p: p.children[1].value, parameters))
        parameter_addresses = list(
            map(lambda p: function_variables[p], parameter_names))
        memory_needed = len(function_variables)
        return_address = None
        if return_type is not None:
            return_address = assign_to_memory(return_type)
        table_entry = {
            "returns": return_address,
            "parameters": parameter_addresses,
            "memory": memory_needed,
            "position": None,
        }
        directory[function_id] = table_entry

from lark import Visitor
from enums import DataTypes


def generate_functions_directory(tree):
    FunctionsDirectory().visit_topdown(tree)
    return FunctionsDirectory.functions_directory


def get_directory(functions_directory, class_context=None):
    directory = functions_directory
    if class_context is not None:
        directory = directory[class_context]
    return directory


def get_function_parameters(parameters_node):
    parameters = []
    while parameters_node is not None:
        declaration_type, var_id, next_parameter = parameters_node.children
        var_type = DataTypes[declaration_type.children[0].value.upper()]
        parameters.append(var_type)
        parameters_node = next_parameter
    return parameters


def get_return_type(return_type):
    if hasattr(return_type, "type"):
        return return_type.value
    return DataTypes[return_type.children[0].value.upper()]


class FunctionsDirectory(Visitor):
    class_context = None
    functions_directory = {}

    def class_declaration(self, tree):
        class_id = tree.children[1].value
        self.class_context = class_id
        if class_id not in self.functions_directory:
            self.functions_directory[class_id] = {}

    def np_end_class_declaration(self, _tree):
        self.class_context = None

    def function_declaration(self, tree):
        return_type, id, parameters, body, _ = tree.children
        function_id = id.value
        parameters = get_function_parameters(parameters)
        directory = get_directory(self.functions_directory, self.class_context)
        return_type = get_return_type(return_type)
        table_entry = {
            "returns": return_type,
            "parameters": parameters
        }
        directory[function_id] = table_entry

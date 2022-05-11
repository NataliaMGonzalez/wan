from lark.visitors import Visitor_Recursive
from enums import DataTypes, FunctionReturnTypes


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

    def class_id(self, tree):
        class_id = tree.children[0].value
        self.get_current_directory()[class_id] = {}
        self.class_context = class_id

    def class_declaration(self, _tree):
        self.class_context = None

    def function_declaration(self, tree):
        return_type, id, *parameters, _body = tree.children
        function_id = id.children[0].value
        directory = self.get_current_directory()
        if function_id in directory:
            raise TypeError(
                "Function \"{}\" already declared in this scope.".format(function_id))
        return_type = FunctionReturnTypes(return_type.value)
        parameters = list(
            map(lambda p: DataTypes(p.children[0].value), parameters))
        table_entry = {
            "returns": return_type,
            "parameters": parameters
        }
        directory[function_id] = table_entry

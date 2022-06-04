from lark import Tree
from lark.visitors import Visitor_Recursive
from collections import OrderedDict
from enums import DataTypes


primitive_types = set(type.value for type in DataTypes)


def generate_classes_variables(tree: Tree):
    ClassesVariables().visit(tree)
    return ClassesVariables.classes_variables


class ClassesVariables(Visitor_Recursive):
    class_context = None
    function_context = None
    classes_variables = OrderedDict()

    def class_id(self, tree: Tree):
        class_id = tree.children[0].value
        self.classes_variables[class_id] = OrderedDict()
        self.class_context = class_id

    def class_inheritance(self, tree: Tree):
        class_id = self.class_context
        parent_id = tree.children[0].value
        parent_table = self.classes_variables[parent_id]
        for key in parent_table:
            if key not in self.classes_variables[class_id]:
                self.classes_variables[class_id][key] = parent_table[key]

    def class_declaration(self, _tree: Tree):
        self.class_context = None

    def function_id(self, tree: Tree):
        function_id = tree.children[0].value
        self.function_context = function_id

    def function_declaration(self, _tree: Tree):
        self.function_context = None

    def vars_declaration(self, tree: Tree):
        """
        Save all of the class attributes in the class variables to later
        retrieve them in class instantiation.
        """
        declaration_type, *declaration_ids = tree.children
        in_class_attributes_context = self.function_context is None and self.class_context is not None
        if not in_class_attributes_context:
            return

        for declaration in declaration_ids:
            var_name, *array_sizes = declaration.children
            var_name = var_name.value
            sizes = list(map(lambda s: int(s.value), array_sizes))
            class_variables = self.classes_variables[self.class_context]
            if var_name in class_variables:
                error_message = "Variable \"{}\" already declared in this scope.".format(
                    var_name)
                raise TypeError(error_message)
            class_variables[var_name] = {
                "name": var_name,
                "type": declaration_type.value,
                "sizes": sizes,
            }
            return

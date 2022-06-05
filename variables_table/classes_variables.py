from lark import Tree
from lark.visitors import Visitor_Recursive
from collections import OrderedDict
from enums import DataTypes


primitive_types = set(type.value for type in DataTypes)


def generate_classes_variables(tree: Tree):
    ClassesVariables().visit(tree)
    return ClassesVariables.classes_variables


class ClassesVariables(Visitor_Recursive):
    """Traverses all the neuralgic points placed accross the grammar in order to
    generate a table with all of the variables for each class.
    """

    # The variables each class contains, to be used when instantiating the classes
    classes_variables = OrderedDict()

    class_context: str = None               # If we are inside a class
    function_context: str = None            # If we are inside a function

    def class_id(self, tree: Tree):
        """Set the class context to indicate we are now inside a class.
        `class_id: CLASS_ID`
        """
        class_id: str = tree.children[0].value
        self.classes_variables[class_id] = OrderedDict()
        self.class_context = class_id

    def class_inheritance(self, tree: Tree):
        """Place all of the variables of the father class into the child.
        `class_id: CLASS_ID`
        """
        class_id = self.class_context
        parent_id: str = tree.children[0].value
        parent_table = self.classes_variables[parent_id]
        for key in parent_table:
            if key not in self.classes_variables[class_id]:
                self.classes_variables[class_id][key] = parent_table[key]

    def class_declaration(self, _tree: Tree):
        """Once we finish traversing the class, indicate that we are now outside.
        `class_id: CLASS_ID`
        """
        self.class_context = None

    def function_id(self, tree: Tree):
        """Set the function context to indicate we are now inside a function.
        \n`function_id: FUNCTION_ID`
        """
        function_id = tree.children[0].value
        self.function_context = function_id

    def function_declaration(self, _tree: Tree):
        """Once we finish traversing the function, indicate that we are now outside.
        `function_declaration: (FUNCTION_DECLARE | declaration_type) function_id _OPEN_GROUP _function_parameters _CLOSE_GROUP _OPEN_BLOCK function_body _CLOSE_BLOCK`
        """
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

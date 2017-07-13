"""
The classes in this file are responsible for processing a dictionary of values
that describe how the pretty-printed and source code versions should be 
generated. This dictionary of values would come from the XMLAdapator class
which would convert from an XMI format to a dictionary.

Output based on this: https://github.com/jasonvan/prexel/blob/master/planning/entry-examples.md
"""

INDENTATION = "    "


class PrettyPrintEncoder:
    def generate_class(self, diagram_element):
        items_to_measure = []

        try:
            name = diagram_element["name"]
        except KeyError as error:
            pass  # TODO deal with this error
        else:
            items_to_measure += [name]

        try:
            methods = diagram_element["methods"]
        except KeyError as error:
            pass  # TODO deal with this error
        else:
            items_to_measure += methods

        try:
            fields = diagram_element["fields"]
        except KeyError as error:
            pass  # TODO deal with this error
        else:
            items_to_measure += fields

        # Determine max length of longest string in class
        max_length = len(max(items_to_measure, key=len))

        # Create the class header and the body
        class_header = self.generate_class_header(max_length, name)
        class_body = self.generate_class_body(max_length, methods)

        return class_header + class_body

    def generate_class_body(self, max_length, methods=[], fields=[]):
        middle_formatter = "|{:<" + str(max_length) + "}|\n"
        bottom_formatter = " {:-^" + str(max_length) + "} \n"

        middle = ""

        for field in fields:
            middle += middle_formatter.format(field)

        for method in methods:
            middle += middle_formatter.format(method)

        bottom = bottom_formatter.format("")

        return middle + bottom

    def generate_class_header(self, max_length, name):
        top_formatter = " {:_^" + str(max_length) + "} \n"
        middle_formatter = "|{:^" + str(max_length) + "}|\n"
        bottom_formatter = "|{:-^" + str(max_length) + "}|\n"

        top = top_formatter.format("")
        middle = middle_formatter.format(name)
        bottom = bottom_formatter.format("")

        return top + middle + bottom


class SourceCodeEncoder:
    def generate_class(self, diagram_element):
        # Process the dictionary values
        try:
            name = diagram_element["name"]
        except KeyError:
            raise Exception("Diagram element must specify a \"name\" key")

        try:
            extends = diagram_element["extends"]
        except KeyError:
            extends = None

        try:
            fields = diagram_element["fields"]
        except KeyError:
            fields = None

        try:
            methods = diagram_element["methods"]
        except KeyError:
            methods = None

        # Format the output
        output = "class {}".format(name)

        if extends:
            output += "({})".format(extends)

        output += ":\n"

        if fields or methods:
            if fields:
                output += INDENTATION + "def __init__(self, {}):\n".format(
                    ", ".join(fields))
                for index, field in enumerate(fields):
                    output += INDENTATION * 2 + "self.{0} = {0}\n".format(field)
                    if index == len(fields) - 1:
                        output += "\n"

            if methods:
                for index, method in enumerate(methods):
                    if type(method) is dict:
                        try:
                            name = method["name"]
                        except KeyError:
                            name = None

                        try:
                            body = method["body"]
                        except KeyError:
                            body = None

                        if name:
                            name = name.replace("()", "")
                            output += INDENTATION + "def {}(self):\n".format(name)

                        if body:
                            output += INDENTATION * 2 + "{}\n".format(body)
                    else:
                        # TODO need to handle method arguments
                        method = method.replace("()", "")
                        output += INDENTATION + "def {}(self):\n".format(method)
                        output += INDENTATION * 2 + "pass\n".format(method)

                    if index != len(methods) - 1:
                        output += "\n"
        else:
            output += INDENTATION + "pass\n"

        return output

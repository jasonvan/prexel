INDENTATION = "    "


class PrettyPrintEncoder:
    """
    TODO
    """
    def generate_class(self, diagram_element):
        """
        TODO
        """
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
        """
        TODO
        """
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
        """
        TODO
        """
        top_formatter = "\n {:_^" + str(max_length) + "} \n"
        middle_formatter = "|{:^" + str(max_length) + "}|\n"
        bottom_formatter = "|{:-^" + str(max_length) + "}|\n"

        top = top_formatter.format("")
        middle = middle_formatter.format(name)
        bottom = bottom_formatter.format("")

        return top + middle + bottom


class SourceCodeEncoder:
    """
    TODO
    """
    def generate_class(self, diagram_element):
        """
        TODO
        """
        try:
            name = diagram_element["name"]
        except KeyError as error:
            pass  # TODO deal with this error

        output = "class {}:\n".format(name)

        try:
            fields = diagram_element["fields"]
        except KeyError as error:
            pass  # TODO deal with this error
        else:
            if fields:
                output += INDENTATION + "def __init__(self, {}):\n".format(
                    ", ".join(fields))
                for index, field in enumerate(fields):
                    output += INDENTATION * 2 + "self.{0} = {0}\n".format(field)
                    if index == len(fields) - 1:
                        output += "\n"

        try:
            methods = diagram_element["methods"]
        except KeyError as error:
            pass  # TODO deal with this error
        else:
            if methods:
                for index, method in enumerate(methods):
                    # TODO need to handle method arguments
                    method = method.replace("()", "")
                    output += INDENTATION + "def {}(self):\n".format(method)
                    output += INDENTATION * 2 + "pass\n".format(method)

                    if index != len(methods) - 1:
                        output += "\n"

        return output

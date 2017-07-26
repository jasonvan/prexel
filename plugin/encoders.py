"""
The classes in this file are responsible for processing a dictionary of values
that describe how the pretty-printed and source code versions should be 
generated. This dictionary of values would come from the XMLAdapator class
which would convert from an XMI format to a dictionary.

Output based on this: https://github.com/jasonvan/prexel/blob/master/planning/entry-examples.md
"""

import re


class PrettyPrintEncoder:
    """
    PrettyPrintEncoder is responsible for taking a diagram element
    and creating a pretty-printed version of the element.
     ----------------------
    |  PrettyPrintEncoder  |
    |----------------------|------>|Diagram
    |generate_class()      |
     ______________________
    """
    def generate_class(self, diagram):
        """
        This method returns a pretty-printed class diagram based on
        the provided diagram object.

        Precondition: Well-formed diagram element
        Returns: pretty-printed diagram
        """

        # Need to measure the different elements of the diagram to see
        # which is the longest string
        items_to_measure = []

        # Name
        items_to_measure.append(diagram.name)

        # Methods
        if diagram.methods:
            for method in diagram.methods:
                items_to_measure.append(method)

        # Fields
        if diagram.fields:
            for field in diagram.fields:
                items_to_measure.append(field)

        # Determine max length of longest string in class
        max_length = len(max(items_to_measure, key=len))

        # Create the class header and the body
        result = ""
        result += self.generate_class_header(max_length, diagram.name)
        result += self.generate_class_body(max_length, diagram)

        return result

    def generate_class_body(self, max_length, diagram):
        """
        Generate the class body string for the provided diagram.

        Returns: class body string
        """

        # Create formatters that will properly space the body string
        middle_formatter = "|{:<" + str(max_length) + "}|\n"
        bottom_formatter = "|{:_^" + str(max_length) + "}|\n"

        # Generate the body string
        body = ""

        if diagram.fields:
            for field in diagram.fields:
                body += middle_formatter.format(field)

        if diagram.methods:
            for method in diagram.methods:
                body += middle_formatter.format(method)

        body += bottom_formatter.format("")

        return body

    def generate_class_header(self, max_length, name):
        """
        Generate the class header from the provided diagram name.

        Returns: class header string
        """

        # Create formatters
        top_formatter = " {:_^" + str(max_length) + "} \n"
        middle_formatter = "|{:^" + str(max_length) + "}|\n"
        bottom_formatter = "|{:-^" + str(max_length) + "}|\n"

        # Generate header string
        header = ""
        header += top_formatter.format("")
        header += middle_formatter.format(name)
        header += bottom_formatter.format("")

        return header


class SourceCodeEncoder:
    """
    SourceCodeEncoder is responsible for taking a diagram element
    and create the appropriate source code.
     ----------------------
    |  SourceCodeEncoder   |
    |----------------------|------>|Diagram
    |generate_class()      |
     ______________________
    """

    def generate_class(self, diagram):
        """
        Generate a class from the provided diagram.

        Returns: a class string
        """

        # Cache diagram values to local variables
        name = diagram.name
        extends = diagram.extends
        fields = diagram.fields
        methods = diagram.methods

        # Set default indentation
        indentation = "    "

        # Argument regex
        method_arguments = re.compile("\({}\)")

        # Format the class output
        result = "class {}".format(name)

        if extends:
            result += "({})".format(extends)

        result += ":\n"

        # Add fields and methods
        if fields or methods:
            # Create a __init__ method if fields are provided
            if fields:
                result += indentation + "def __init__(self, {}):\n".format(
                    ", ".join(fields))
                for index, field in enumerate(fields):
                    result += indentation * 2 + "self.{0} = {0}\n".format(field)
                    if index == len(fields) - 1:
                        result += "\n"

            # Create methods if methods values are provided
            if methods:
                for index, method in enumerate(methods):
                    # If a dictionary is provided for method process the
                    # extra information.
                    if type(method) is dict:
                        # TODO need to handle method arguments
                        # Check for name key in dict
                        try:
                            name = method["name"]
                        except KeyError:
                            pass
                        else:
                            argument = str(name)
                            name = name.replace("()", "")
                            result += indentation + "def {}(self):\n".format(name)

                        # Check for body key in dict
                        try:
                            body = method["body"]
                        except KeyError:
                            pass  # Don't do anything if body is missin
                            # body = None
                        else:
                            result += indentation * 2 + "{}\n".format(body)
                    else:
                        # Process method as is since no dictionary was provided
                        # TODO need to handle method arguments
                        method = method.replace("()", "")
                        result += indentation + "def {}(self):\n".format(method)
                        result += indentation * 2 + "pass\n".format(method)

                    if index != len(methods) - 1:
                        result += "\n"
        else:
            result += indentation + "pass\n"

        # Add a newline after class
        result += "\n"

        return result

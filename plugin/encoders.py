"""
The classes in this file are responsible for processing a dictionary of values
that describe how the pretty-printed and source code versions should be 
generated. This dictionary of values comes from the XMLAdapator class
which would convert from an XMI format to a dictionary.

Output based on:
https://github.com/jasonvan/prexel/blob/master/planning/entry-examples.md
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
        items_to_measure = list()

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


class SourceCodeEncoderException(Exception):
    pass


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
    method_signature_regex = re.compile(r'([^(){}]*)\((.*)\)')
    indentation = "    "

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

        # Format the class output
        result = "class {}".format(name)

        # Add super class if it has one
        if extends:
            result += "({})".format(extends)

        result += ":\n"

        # Add fields and methods
        if fields or methods:
            # Create a __init__ method if fields are provided
            if fields:
                result += SourceCodeEncoder.indentation + \
                          "def __init__(self, {}):\n".format(", ".join(fields))

                for index, field in enumerate(fields):
                    result += SourceCodeEncoder.indentation * 2 + \
                              "self.{0} = {0}\n".format(field)
                    if index == len(fields) - 1:
                        result += "\n"

            # Create methods if methods values are provided
            if methods:
                for index, method in enumerate(methods):
                    # Process extra method information if dictionary
                    # of values is provided.
                    if type(method) is dict:

                        # Method signature
                        try:
                            signature = method["signature"]
                            result += self.process_method_signature(signature)
                        except (KeyError, SourceCodeEncoderException):
                            continue  # Proceed to next method if any errors

                        # Method body
                        try:
                            body = method["body"]
                        except KeyError:
                            continue
                        else:
                            result += SourceCodeEncoder.indentation * 2 + \
                                "{}\n".format(body)
                    # Just a string so create an empty method
                    else:
                        try:
                            result += self.process_method_signature(method)
                            result += SourceCodeEncoder.indentation * 2 + \
                                "pass\n"
                        except SourceCodeEncoderException:
                            continue

                    if index != len(methods) - 1:
                        result += "\n"
        # Output pass if no fields or methods provided
        else:
            result += SourceCodeEncoder.indentation + "pass\n"

        # Add a newline after class
        result += "\n"

        return result

    @staticmethod
    def process_method_signature(signature):
        """
        Processes the method signature for method name and parameters

        Returns: string version of method
        """
        matcher = SourceCodeEncoder.method_signature_regex.match(signature)

        if not matcher:
            raise SourceCodeEncoderException("Method signature not "
                                             "properly formatted.")

        method_name, method_arguments = matcher.groups()

        result = ""
        result += SourceCodeEncoder.indentation + \
            "def {}(self".format(method_name)

        if method_arguments.strip():
            result += ", {}".format(method_arguments)

        result += "):\n"

        return result

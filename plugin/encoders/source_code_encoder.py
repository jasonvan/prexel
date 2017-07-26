"""
The classes in this file are responsible for processing a dictionary of values
that describe how the pretty-printed and source code versions should be 
generated. This dictionary of values comes from the XMLAdapator class
which would convert from an XMI format to a dictionary.

Output based on:
https://github.com/jasonvan/prexel/blob/master/planning/entry-examples.md
"""

import re


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


class SourceCodeEncoderException(Exception):
    pass

from prexel.encoders.encoder import Encoder
from prexel.regex import REGEX

# TODO - make this configurable
INDENTATION = "    "  # Default indentation


class SourceCodeEncoder(Encoder):
    """
    SourceCodeEncoder is responsible for taking a diagram element
    and create the appropriate source code output.

    Output based on:
    https://github.com/jasonvan/prexel/blob/master/planning/entry-examples.md

     _______ 
    |Encoder|
    |_______|
    ∆
    |_________________ 
    |SourceCodeEncoder|
    |-----------------|
    |generate()       |
    |create_class()   |
    |_________________|

    """
    def generate(self, diagram):
        """
        TODO change this to return an array of tuples,
        with class_name, and contents
        TODO comment this code
        """
        classes = []
        parent_name = None

        if diagram.parent:
            parent = SourceCodeEncoder.create_class(diagram.parent)
            parent_name = diagram.parent.name
            parent_tup = (parent_name.lower(), parent)
            classes.append(parent_tup)

        if diagram.aggregated and diagram.aggregation:
            aggregated = SourceCodeEncoder.create_class(diagram.aggregated)
            aggregated_tup = (diagram.aggregated.name.lower(),aggregated)
            classes.append(aggregated_tup)

        main = SourceCodeEncoder.create_class(diagram.main, parent_name)
        main_tup = (diagram.main.name.lower(), main)

        classes.append(main_tup)

        return classes

    @staticmethod
    def create_class(diagram, extends=None):
        """
        Generate a class from the provided diagram.
        Returns: a class string
        """

        # Cache diagram values to local variables
        name = diagram.name
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
                result += INDENTATION + \
                          "def __init__(self, {}):\n".format(", ".join(fields))

                for index, field in enumerate(fields):
                    result += INDENTATION * 2 + \
                        "self.{0} = {0}\n".format(field)

                    if index == len(fields) - 1 and methods:
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
                            result += SourceCodeEncoder.process_method_signature(signature)
                        except (KeyError, SourceCodeEncoderException):
                            continue  # Proceed to next method if any errors

                        # Method body
                        try:
                            body = method["body"]
                        except KeyError:
                            continue
                        else:
                            result += INDENTATION * 2 + "{}\n".format(body)
                    # Just a string so create an empty method
                    else:
                        try:
                            result += SourceCodeEncoder.process_method_signature(method)
                            result += INDENTATION * 2 + "pass\n"
                        except SourceCodeEncoderException:
                            continue

                    if index != len(methods) - 1:
                        result += "\n"
        # Output pass if no fields or methods provided
        else:
            result += INDENTATION + "pass\n"

        # TODO - might need to add this back in to add a newline after class
        # result += "\n"

        return result

    @staticmethod
    def process_method_signature(signature):
        """
        Processes the method signature for method name and parameters
        Returns: string version of method
        """
        matcher = REGEX["method_signature"].match(signature)

        if not matcher:
            raise SourceCodeEncoderException("Method signature not "
                                             "properly formatted.")

        method_name, method_arguments = matcher.groups()

        result = ""
        result += INDENTATION + \
            "def {}(self".format(method_name)

        if method_arguments.strip():
            result += ", {}".format(method_arguments)

        result += "):\n"

        return result


class SourceCodeEncoderException(Exception):
    pass

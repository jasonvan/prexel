from prexel.encoders.encoder import Encoder
from prexel.regex import REGEX

# Load sublime if inside of sublime text
try:
    import sublime
except ImportError:
    sublime_imported = False
else:
    sublime_imported = True


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

        classes.append(
            (diagram.name.lower(), SourceCodeEncoder.create_class(diagram))
        )

        if diagram.sub_classes:
            for sub_class in diagram.sub_classes:
                classes.append(
                    (sub_class.name.lower(), SourceCodeEncoder.create_class(sub_class, diagram.name))
                )

                self.generate_aggregated_classes(sub_class, classes)
                #
                # if sub_class.aggregated_classes:
                #     for aggregated_class in diagram.aggregated_classes:
                #         classes.append(
                #             (aggregated_class.name.lower(), SourceCodeEncoder.create_class(aggregated_class))
                #         )

        self.generate_aggregated_classes(diagram, classes)
        # if diagram.aggregated_classes:
        #     for aggregated_class in diagram.aggregated_classes:
        #         classes.append(
        #             (aggregated_class.name.lower(), SourceCodeEncoder.create_class(aggregated_class))
        #         )

        return classes

    def generate_aggregated_classes(self, diagram, class_list):
        if diagram.aggregated_classes:
            for aggregated_class in diagram.aggregated_classes:
                class_list.append(
                    (aggregated_class.name.lower(), SourceCodeEncoder.create_class(aggregated_class))
                )

    @staticmethod
    def create_class(diagram, extends=None):
        """
        Generate a class from the provided diagram.
        Returns: a class string
        """

        # Get indentation value
        indentation = SourceCodeEncoder.get_user_defined_identation()

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
                result += indentation + \
                          "def __init__(self, {}):\n".format(", ".join(fields))

                for index, field in enumerate(fields):
                    result += indentation * 2 + \
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
                            result += indentation * 2 + "{}\n".format(body)
                    # Just a string so create an empty method
                    else:
                        try:
                            result += SourceCodeEncoder.process_method_signature(method)
                            result += indentation * 2 + "pass\n"
                        except SourceCodeEncoderException:
                            continue

                    if index != len(methods) - 1:
                        result += "\n"
        # Output pass if no fields or methods provided
        else:
            result += indentation + "pass\n"

        return result

    @staticmethod
    def process_method_signature(signature):
        """
        Processes the method signature for method name and parameters
        Returns: string version of method
        """
        # Get indentation value
        indentation = SourceCodeEncoder.get_user_defined_identation()

        matcher = REGEX["method_signature"].match(signature)

        if not matcher:
            raise SourceCodeEncoderException("Method signature not "
                                             "properly formatted.")

        method_name, method_arguments = matcher.groups()

        result = ""
        result += indentation + \
            "def {}(self".format(method_name)

        if method_arguments.strip():
            result += ", {}".format(method_arguments)

        result += "):\n"

        return result

    @staticmethod
    def get_user_defined_identation():
        """
        Retrieves the user-defined indentation value if it was set inside
        of Prexel.sublime-settings
        """

        indentation = "    "  # Default value

        # Only add if we are inside of Sublime Text
        if sublime_imported:
            settings = sublime.load_settings('Prexel.sublime-settings')
            indentation_value = settings.get('indentation')

            if indentation_value:
                indentation = indentation_value

        return indentation


class SourceCodeEncoderException(Exception):
    pass

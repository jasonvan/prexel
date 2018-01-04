"""
Code in this class is based on https://ruslanspivak.com/lsbasi-part6/
"""
from prexel.parser.lexer import Token
from prexel.encoders.xmi_encoder import XMIDocumentGenerator
from prexel.models.diagram import (Diagram, AggregationDiagram,
                                   AggregationMultiplicity)


class Interpreter:

    """
     _____________              _____ 
    | Interpreter |<>-lexer--->|Lexer|
    |-------------|            |-----|
    |current_token|            |text |
    |lexer        |            |_____|
    |evaluate()   |                   
    |_____________|                   

    The Interpreter class processes the token stream received from the 
    Lexer class. A diagram object is returned from the evaluate() method 
    of this class.
     ___________________
    |      Diagram      |
    |-------------------|
    |name               |
    |fields             |
    |methods            |
    |sub_classes        |
    |aggregated_classes |
    |___________________|

    A Diagram object is used by the encoders to generate pretty-printed, and 
    optionally, source code versions of the diagram.
     __________________ 
    |PrettyPrintEncoder|
    |------------------|
    |generate(diagram) |
    |__________________|

     _________________ 
    |SourceCodeEncoder|
    |-----------------|
    |generate(diagram)|
    |_________________|

     _________________ 
    |   XMIEncoder    |
    |-----------------|
    |generate(diagram)|
    |_________________|

    """
    
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_token()
        self.generator = XMIDocumentGenerator()

    def error(self, message="Invalid Syntax"):
        """
        Raises a InterpreterException for processing later.
        """
        raise InterpreterException(message)

    def process_token(self, token_type):
        """
        Process a single token from the lexer. An error is thrown
        if the current token type doesn't match the token type passed to
        this method.
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_token()
        else:
            self.error()

    def start_marker(self):
        """
        Process a START_MARKER token. This token is denoted by "|" and defines
        the beginning of a easy-entry string
        """
        self.process_token(Token.START_MARKER)

    def class_name(self):
        """
        Process a CLASS_NAME token and return the name
        """

        # Process Token
        name = self.current_token.value
        self.process_token(Token.CLASS_NAME)
        return name

    def class_body(self):
        """
        Process FIELD and METHOD tokens
        """
        fields = []
        methods = []

        while self.current_token and self.current_token.type in (Token.FIELD,
                                                                 Token.METHOD):
            token = self.current_token

            # Process FIELD token
            if token.type == Token.FIELD:
                # Append the token value
                fields.append(token.value)

                # Process token
                self.process_token(Token.FIELD)

            # Process METHOD token
            if token.type == Token.METHOD:
                # Append the token value
                methods.append(token.value)

                # Process token
                self.process_token(Token.METHOD)

        return fields, methods

    def next_token_is_class_token(self):
        """
        Helper method to check whether the next token is a CLASS_NAME token.
        """
        return self.current_token and \
            self.current_token.type is Token.CLASS_NAME

    def inheritance(self):
        """
        Process an INHERITANCE TOKEN.
        """
        has_inheritance = False

        if self.current_token and self.current_token.type is Token.INHERITANCE:
            # Process token
            self.process_token(Token.INHERITANCE)

            # Check CLASS_NAME token follows the INHERITANCE token
            if self.next_token_is_class_token():
                has_inheritance = True
            else:
                self.error("Missing child class after \">>\"")

        return has_inheritance

    def class_delimiter(self):
        """
        Process a COMMA token which acts as a delimiter between classes
        """
        if self.current_token and self.current_token.type is Token.COMMA:
            # Process COMMA token
            self.process_token(Token.COMMA)

            # Confirm that a CLASS_NAME token follows the AGGREGATION token
            if not self.next_token_is_class_token():
                self.error("The is no following class name.")

            return True

        return False

    def aggregation(self, include_following_tokens=True):
        """
        Process an AGGREGATION token and returns a dictionary of values.
        """
        aggregation = {}

        if self.current_token and self.current_token.type is Token.AGGREGATION:
            # Cache the current token
            token = self.current_token

            # Process AGGREGATION token
            self.process_token(Token.AGGREGATION)

            # Confirm that a CLASS_NAME token follows the AGGREGATION token
            if not self.next_token_is_class_token():
                self.error("There is no class name following the aggregation.")

            # Aggregated Class name
            aggregation["name"] = self.class_name()

            # TODO do we still need multiline syntax?
            # Multi-line with aggregation
            # |Class1 <>-> Class2
            # |class_1_field
            # |class_1_method()
            if include_following_tokens:
                fields, methods = self.class_body()
                aggregation["fields"] = fields
                aggregation["methods"] = methods

            # Check that the AGGREGATION token has a name, if not
            # default to the aggregated class's name
            name = token.value["name"]
            if name:
                aggregation["instance_name"] = name
            else:
                generated_name = aggregation["name"].lower()
                aggregation["instance_name"] = generated_name

            # Add multiplicity values
            aggregation["left_multi"] = token.value["left_multi"]
            aggregation["right_multi"] = token.value["right_multi"]

        return aggregation

    def add_optional_aggregation(self, diagram):
        aggregation = self.aggregation()
        if aggregation:
            aggregated_diagram = AggregationDiagram()

            # Need to clear out the fields and methods arrays as
            # Sublime Text keeps the objects around
            aggregated_diagram.fields = []
            aggregated_diagram.methods = []

            try:
                name = aggregation["name"]
                aggregated_diagram.name = name
            except KeyError:
                pass

            try:
                fields = aggregation["fields"]
                aggregated_diagram.add_fields(fields)
            except KeyError:
                pass

            try:
                methods = aggregation["methods"]
                aggregated_diagram.add_methods(methods)
            except KeyError:
                pass

            try:
                instance_name = aggregation["instance_name"]
                aggregated_diagram.instance_name = instance_name
            except KeyError:
                pass

            try:
                left_multi = aggregation["left_multi"]
                right_multi = aggregation["right_multi"]

                aggregated_diagram.left_multiplicity = left_multi
                aggregated_diagram.right_multiplicity = right_multi
            except KeyError:
                pass

            # Add the aggregated class to current class diagram
            diagram.add_aggregated_class(aggregated_diagram)

    def evaluate(self):
        """
        Main evaluation method. This methods processes the tokens based on
        set grammar.
        """
        # Check for the first PREXEL marker
        self.start_marker()

        # Process class name, fields, and methods
        name = self.class_name()
        fields, methods = self.class_body()

        # Create main Diagram object
        main_diagram = Diagram(name, fields, methods)

        # Optional - Check for inheritance
        if self.inheritance():
            has_parent_class = True
        else:
            has_parent_class = False

        # Process the rest of the possible classes
        self.add_optional_aggregation(main_diagram)

        while self.current_token:
            if not self.class_delimiter():
                # Process class name, fields, and methods
                name = self.class_name()
                fields, methods = self.class_body()

                # Create Diagram object for current class
                diagram = Diagram(name, fields, methods)

                # Check aggregation values
                self.add_optional_aggregation(diagram)

                # If there is a parent class add the current class
                # as a subclass
                if has_parent_class:
                    main_diagram.add_sub_class(diagram)

        # TODO discuss what we should do with this
        # Optional - Check for aggregation but don't
        # consider the fields and methods following the aggregation
        # token as part of the aggregated class.In this position
        # they belong to the main class
        # self.aggregation(include_following_tokens=False)

        return main_diagram


class InterpreterException(Exception):
    pass

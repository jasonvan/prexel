"""
Code in this class is based on https://ruslanspivak.com/lsbasi-part6/
"""
from prexel.parser.lexer import Token
from prexel.models.diagram import (Diagram,
                                   ClassDiagramPart,
                                   AggregationDiagramPart,
                                   InheritanceDiagramPart)


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
     ___________ 
    |  Diagram  |
    |-----------|
    |main       |
    |parent     |
    |inheritance|
    |aggregated |
    |aggregation|
    |___________|

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

    """
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_token()

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

    def class_name(self, class_diagram_part):
        """
        Process a CLASS_NAME token and set the name value on a 
        ClassDiagramPart object which it inherits from the DiagramPart class.

         ___________ 
        |DiagramPart|
        |-----------|
        |name       |
        |type       |
        |___________|
        ∆
        |________________ 
        |ClassDiagramPart|
        |----------------|
        |fields          |
        |methods         |
        |extends         |
        |________________|

        """
        class_diagram_part.name = self.current_token.value

        # Process Token
        self.process_token(Token.CLASS_NAME)

    def class_body(self, class_diagram_part):
        """
        Process the fields and method for a ClassDiagramPart object.
        """
        while self.current_token and self.current_token.type in (Token.FIELD, Token.METHOD):
            token = self.current_token

            # Process FIELD token
            if token.type == Token.FIELD:
                # Create list for fields if it doesn't exist
                if not class_diagram_part.fields:
                    class_diagram_part.fields = []

                # Append the token value
                class_diagram_part.fields.append(token.value)

                # Process token
                self.process_token(Token.FIELD)

            # Process METHOD token
            if token.type == Token.METHOD:
                # Create list for methods if is doesn't exist
                if not class_diagram_part.methods:
                    class_diagram_part.methods = []

                # Append the token value
                class_diagram_part.methods.append(token.value)

                # Process token
                self.process_token(Token.METHOD)

    def next_token_is_class_token(self):
        """
        Helper method to check whether the next token is a CLASS_NAME token.
        """
        return self.current_token and self.current_token.type is Token.CLASS_NAME

    def inheritance(self, diagram):
        """
        Process an INHERITANCE TOKEN. Sets the parent and inheritance fields
        on the Diagram object.

         ___________               ________________ 
        |  Diagram  |<>-parent--->|ClassDiagramPart|
        |-----------|             |________________|
        |inheritance|                               
        |parent     |                               
        |___________|                               

        """
        if self.current_token and self.current_token.type is Token.INHERITANCE:
            # Make sure that a class name token follows an inheritance token
            inheritance = InheritanceDiagramPart()

            # Process token
            self.process_token(Token.INHERITANCE)

            # Check is CLASS_NAME token follows the INHERITANCE token
            if self.next_token_is_class_token():
                parent = ClassDiagramPart()

                # Determine parent class name
                self.class_name(parent)

                # Append inheritance diagram and then parent class diagram
                diagram.inheritance = inheritance
                diagram.parent = parent
            else:
                self.error("Missing parent class after \"<<\"")

    def aggregation(self, diagram, include_following_tokens=True):
        """
        Process an AGGREGATION token
        # TODO comment and clean up
        """
        if self.current_token and self.current_token.type is Token.AGGREGATION:
            token = self.current_token
            self.process_token(Token.AGGREGATION)

            if not self.next_token_is_class_token():
                self.error()

            if not diagram.main.fields:
                diagram.main.fields = []

            name = token.value["name"]

            aggregation = AggregationDiagramPart()

            if name:
                diagram.main.fields.append(name)
                aggregation.name = name
            else:
                # TODO - need to handle missing aggregated value
                diagram.main.fields.append("MISSING-AGGREGATED-NAME")

            aggregation.left_multiplicity = token.value["left_multi"]
            aggregation.right_multiplicity = token.value["right_multi"]

            diagram.aggregation = aggregation

            # Create aggregated class
            aggregated = ClassDiagramPart()
            self.class_name(aggregated)

            # Optionally include class body
            if include_following_tokens:
                self.class_body(aggregated)

            diagram.aggregated = aggregated

    def evaluate(self):
        diagram = Diagram(main=ClassDiagramPart())

        # Check for the first PREXEL marker
        self.start_marker()

        # Process main class name
        self.class_name(diagram.main)

        # Optional - Check for inheritance
        self.inheritance(diagram)

        # Optional - Check for aggregation but don't
        # consider the fields and methods following the aggregation
        # token as part of the aggregated class.In this position
        # they belong to the main class
        self.aggregation(diagram, include_following_tokens=False)

        # Process fields and methods for main class
        self.class_body(diagram.main)

        # Optional - Check for aggregation
        self.aggregation(diagram)

        return diagram


class InterpreterException(Exception):
    pass

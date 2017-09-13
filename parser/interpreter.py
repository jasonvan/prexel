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
        self.diagram = Diagram()

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

    def class_body(self, class_diagram_part):
        """
        Process the fields and method on a ClassDiagramPart object.
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

    def inheritance(self):
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
        has_inheritance = False

        if self.current_token and self.current_token.type is Token.INHERITANCE:
            inheritance = InheritanceDiagramPart()

            # Process token
            self.process_token(Token.INHERITANCE)

            # Check CLASS_NAME token follows the INHERITANCE token
            if self.next_token_is_class_token():
                child = ClassDiagramPart()

                # Determine child class name
                child.name = self.class_name()

                # Append inheritance diagram and then parent class diagram
                self.diagram.inheritance = inheritance
                self.diagram.main = child
                has_inheritance = True
            else:
                self.error("Missing child class after \">>\"")

        return has_inheritance

    def aggregation(self, include_following_tokens=True):
        """
        Process any aggregated classes. The class process both the AGGREGATION token and
        a CLASS_NAME token for the aggregated class.
        """
        if self.current_token and self.current_token.type is Token.AGGREGATION:
            # Cache the current token
            token = self.current_token

            # Process AGGREGATION Token
            self.process_token(Token.AGGREGATION)

            # Confirm that a CLASS_NAME token follows the AGGREGATION TOKEN
            if not self.next_token_is_class_token():
                self.error("There is no class name following the aggregation.")

            # Process aggregated ClassDiagramPart. Optionally include class body
            aggregated = ClassDiagramPart()
            aggregated.name = self.class_name()

            if include_following_tokens:
                self.class_body(aggregated)

            self.diagram.aggregated = aggregated

            # Process AggregationDiagramPart
            aggregation = AggregationDiagramPart()

            # Create a list for the fields on the main ClassDiagramPart object
            if not self.diagram.main.fields:
                self.diagram.main.fields = []

            # Check that the AGGREGATION token has a name, if not
            # default to the aggregated class's name
            name = token.value["name"]
            if name:
                self.diagram.main.fields.append(name)
                aggregation.name = name
            else:
                # Generate an aggregation name from the aggregated class
                generated_name = aggregated.name.lower()
                self.diagram.main.fields.append(generated_name)
                aggregation.name = generated_name

            # Add multiplicity values
            aggregation.left_multiplicity = token.value["left_multi"]
            aggregation.right_multiplicity = token.value["right_multi"]

            # Save aggregation value to Diagram object
            self.diagram.aggregation = aggregation

    def evaluate(self):
        # Check for the first PREXEL marker
        self.start_marker()

        # Process the first class name
        first_class_diagram = ClassDiagramPart()
        first_class_diagram.name = self.class_name()

        # Optionally check for FIELD and METHOD tokens
        self.class_body(first_class_diagram)

        # Optional - Check for inheritance
        if self.inheritance():
            self.diagram.parent = first_class_diagram
        else:
            self.diagram.main = first_class_diagram

        # Optional - Check for aggregation but don't
        # consider the fields and methods following the aggregation
        # token as part of the aggregated class.In this position
        # they belong to the main class
        self.aggregation(include_following_tokens=False)

        # Process fields and methods for main class
        self.class_body(self.diagram.main)

        # Optional - Check for aggregation
        self.aggregation()

        return self.diagram


class InterpreterException(Exception):
    pass

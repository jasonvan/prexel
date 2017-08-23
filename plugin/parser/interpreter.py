"""
Code in this class is based on https://ruslanspivak.com/lsbasi-part6/
"""
from prexel.plugin.parser.lexer import Token
from prexel.plugin.models.diagram import (ClassDiagram,
                                          AggregationDiagram,
                                          InheritanceDiagram)


class Interpreter:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_token()
        self.diagrams = []

    def error(self, message="Invalid Syntax"):
        raise InterpreterException(message)

    def process_token(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_token()
        else:
            self.error()

    def start_marker(self):
        self.process_token(Token.PREXEL_MARKER)

    def class_name(self, diagram):
        token = self.current_token
        diagram.name = token.value
        self.process_token(Token.CLASS_NAME)

    def next_token_is_class_token(self):
        return self.current_token and self.current_token.type is Token.CLASS_NAME

    def class_body(self, diagram):
        while self.current_token and self.current_token.type in (Token.FIELD, Token.METHOD):
            token = self.current_token
            if token.type == Token.FIELD:
                if not diagram.fields:
                    diagram.fields = []

                diagram.fields.append(token.value)
                self.process_token(Token.FIELD)
            elif token.type == Token.METHOD:
                if not diagram.methods:
                    diagram.methods = []
                diagram.methods.append(token.value)
                self.process_token(Token.METHOD)

    def inheritance(self):
        # TODO comment and clean up
        if self.current_token and self.current_token.type is Token.INHERITANCE:
            self.process_token(Token.INHERITANCE)
            inheritance_diagram = InheritanceDiagram()

            # Make sure that a class name follows an inheritance token
            if self.next_token_is_class_token():
                parent_class_diagram = ClassDiagram()

                # Determine parent class name
                self.class_name(parent_class_diagram)

                # Append inheritance diagram and then parent class diagram
                self.diagrams.append(inheritance_diagram)
                self.diagrams.append(parent_class_diagram)
            else:
                self.error("Missing parent class after \"<<\"")

    def aggregation(self, diagram, include_class_body=True):
        # TODO comment and clean up
        if self.current_token and self.current_token.type is Token.AGGREGATION:
            token = self.current_token
            self.process_token(Token.AGGREGATION)

            if not self.next_token_is_class_token():
                self.error()

            if not diagram.fields:
                diagram.fields = []

            name = token.value["name"]

            if name:
                diagram.fields.append(name)
            else:
                # TODO - need to handle missing aggregated value
                diagram.fields.append("MISSING-AGGREGATED-NAME")

            aggregation_diagram = AggregationDiagram()
            # TODO - currently this is not used but will be in the future
            aggregation_diagram.left_multiplicity = token.value["left_multi"]
            aggregation_diagram.right_multiplicity = token.value["right_multi"]

            self.diagrams.append(aggregation_diagram)

            # Create aggregated class
            aggregated_class_diagram = ClassDiagram()
            self.class_name(aggregated_class_diagram)

            # Optionally include class body
            if include_class_body:
                self.class_body(aggregated_class_diagram)

            self.diagrams.append(aggregated_class_diagram)

    def evaluate(self):
        # Check for the first PREXEL marker
        self.start_marker()

        # Create main class
        class_diagram = ClassDiagram()
        self.diagrams.append(class_diagram)
        self.class_name(class_diagram)

        # Optional - Check for inheritance
        self.inheritance()

        # Optional - Check for aggregation but don't
        # consider the following fields and methods as part of the
        # aggregated class.In this position they belong to the main class
        self.aggregation(class_diagram, include_class_body=False)

        # Interpret class fields and methods for main class
        self.class_body(class_diagram)

        # Optional - Check for aggregation
        self.aggregation(class_diagram)

        return self.diagrams


class InterpreterException(Exception):
    pass

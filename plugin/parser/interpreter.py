from prexel.plugin.parser.lexer import Token
from prexel.plugin.models.diagram import Diagram


class Interpreter:
    """
    Code referenced from https://ruslanspivak.com/lsbasi-part6/
    TODO: need to comment this code
    """
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_token()

    def error(self):
        raise InterpreterException('Invalid Syntax')

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
        diagram = None

        if self.current_token and self.current_token.type is Token.INHERITANCE:
            token = self.current_token
            self.process_token(Token.INHERITANCE)

            diagram = Diagram()
            diagram.diagram_type = "inheritance"

        return diagram

    def aggregation(self, diagram):
        has_aggregation = False

        if self.current_token and self.current_token.type is Token.AGGREGATION:
            token = self.current_token
            self.process_token(Token.AGGREGATION)
            has_aggregation = True

            if not diagram.fields:
                diagram.fields = []

            name = token.value["name"]

            if name:
                diagram.fields.append(name)
            else:
                # TODO - need to handle missing aggregated value
                diagram.fields.append("MISSING-AGGREGATED-NAME")

            # TODO - currently this is not used but will be in the future
            left_multi = token.value["left_multi"]
            right_multi = token.value["right_multi"]

        return has_aggregation

    def evaluate(self):
        # TODO - clean up and comment this code, a little hard to follow
        # TODO add diagrams as a class variable
        self.start_marker()
        diagrams = []

        first_diagram = Diagram()
        diagrams.append(first_diagram)

        self.class_name(first_diagram)
        inheritance_diagram = self.inheritance()
        if inheritance_diagram:
            # TODO move this check to a method
            if self.current_token and self.current_token.type is Token.CLASS_NAME:
                self.class_name(inheritance_diagram)
                diagrams.append(inheritance_diagram)
            else:
                self.error()  # TODO send error string with message
        self.class_body(first_diagram)
        has_aggregation = self.aggregation(first_diagram)

        if self.current_token and self.current_token.type is Token.CLASS_NAME:
            second_diagram = Diagram()
            self.class_name(second_diagram)
            self.class_body(second_diagram)
            diagrams.append(second_diagram)
        elif has_aggregation:
            # If there is aggregation in the string but not another
            # class afterwards, throw error
            self.error()  # TODO send error string with message

        return diagrams


class InterpreterException(Exception):
    pass

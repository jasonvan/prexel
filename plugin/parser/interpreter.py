from prexel.plugin.parser.lexer import Token
from prexel.plugin.models.diagram import Diagram


class Interpreter:
    """
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

    def prexel(self):
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

    def aggregation(self, diagram):
        while self.current_token and self.current_token.type is Token.AGGREGATION:
            token = self.current_token
            self.process_token(Token.AGGREGATION)

            try:
                left_multi = token.value["left_multi"]
                # TODO - need to use this for something
            except KeyError:
                pass  # TODO

            try:
                name = token.value["name"]
            except KeyError:
                pass  # TODO
            else:
                diagram.fields.append(name)

            try:
                right_multi = token.value["right_multi"]
            except KeyError:
                # TODO - need to use this for something
                pass  # TODO

    def expr(self):
        """
        TODO
        :return:
        """
        self.prexel()
        diagrams = []

        first_diagram = Diagram()

        self.class_name(first_diagram)
        self.class_body(first_diagram)
        self.aggregation(first_diagram)

        diagrams.append(first_diagram)

        if self.current_token and self.current_token.type is Token.CLASS_NAME:
            second_diagram = Diagram()
            self.class_name(second_diagram)
            self.class_body(second_diagram)
            diagrams.append(second_diagram)

        return diagrams


class InterpreterException(Exception):
    pass

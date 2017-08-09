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

    def class_name(self):
        token = self.current_token
        self.process_token(Token.CLASS_NAME)
        return token.value

    def expr(self):
        """
        TODO
        :return:
        """
        self.prexel()

        diagram = Diagram(self.class_name())

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

        # TODO Put aggregation here

        # TODO put optional class reference here

        return diagram


class InterpreterException(Exception):
    pass

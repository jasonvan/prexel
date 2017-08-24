from .parser.lexer import Lexer
from .parser.interpreter import Interpreter, InterpreterException
from .encoders.pretty_print_encoder import PrettyPrintEncoder
from .encoders.source_code_encoder import SourceCodeEncoder


def main():
    while True:
        text = input("Enter easy-entry string: ")

        if not text:
            return

        lexer = Lexer(text)
        interpreter = Interpreter(lexer)

        try:
            diagrams = interpreter.evaluate()
        except InterpreterException as e:
            print(e)
        else:
            for diagram in diagrams:
                encoder = PrettyPrintEncoder()
                print(encoder.create_class(diagram))

            for diagram in diagrams:
                encoder = SourceCodeEncoder()
                print(encoder.create_class(diagram))

if __name__ == '__main__':
    main()

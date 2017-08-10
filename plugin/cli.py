from prexel.plugin.parser.lexer import Lexer
from prexel.plugin.parser.interpreter import Interpreter, InterpreterException
from prexel.plugin.encoders.pretty_print_encoder import PrettyPrintEncoder
from prexel.plugin.encoders.source_code_encoder import SourceCodeEncoder


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
                print(encoder.generate_class(diagram))

            for diagram in diagrams:
                encoder = SourceCodeEncoder()
                print(encoder.generate_class(diagram))

if __name__ == '__main__':
    main()

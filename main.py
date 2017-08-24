import sublime
import sublime_plugin

from prexel.parser.lexer import Lexer
from prexel.parser.interpreter import Interpreter, InterpreterException
from prexel.encoders.pretty_print_encoder import PrettyPrintEncoder
from prexel.encoders.source_code_encoder import SourceCodeEncoder

"""

"""

class GenerateUmlCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Get the currently selected line or lines
        line = self.view.line(self.view.sel()[0])
        text = self.view.substr(line)

        # Create tokens from the text
        lexer = Lexer(text)

        # Interpret the tokens and create a diagram object
        interpreter = Interpreter(lexer)
        diagram = interpreter.evaluate()

        # Encode diagram for output to the view
        encoder = PrettyPrintEncoder()
        result = encoder.generate(diagram)

        # Replace selection
        self.view.replace(edit, line, result)

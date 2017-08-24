import sublime
import sublime_plugin

from .parser.lexer import Lexer
from .parser.interpreter import Interpreter, InterpreterException
from .encoders.pretty_print_encoder import PrettyPrintEncoder
from .encoders.source_code_encoder import SourceCodeEncoder

"""
|Kitchen << Room
"""

class GenerateUmlCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                region_text = self.view.substr(region)

                lexer = Lexer(region_text)
                interpreter = Interpreter(lexer)

                diagram = interpreter.evaluate()
                encoder = PrettyPrintEncoder()

                result = encoder.generate(diagram)

                print(result)
                # TODO Do string processing here

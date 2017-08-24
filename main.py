import sublime
import sublime_plugin

from prexel.parser.lexer import Lexer
from prexel.parser.interpreter import Interpreter, InterpreterException
from prexel.encoders.pretty_print_encoder import PrettyPrintEncoder
from prexel.encoders.source_code_encoder import SourceCodeEncoder

"""
https://stackoverflow.com/questions/30443820/insert-text-into-view-in-sublime-3-api
https://cnpagency.com/blog/creating-sublime-text-3-plugins-part-1/
https://cnpagency.com/blog/creating-sublime-text-3-plugins-part-2/
http://techsideonline.com/sublime-text-3-plugin/
https://www.sublimetext.com/docs/3/api_reference.html#sublime.Edit
Important locations
/Applications/Sublime Text.app/Contents/MacOS/Packages/default
WINDOWS — %APPDATA%\Sublime Text 3\Packages
LINUX — ~/.config/sublime-text-3/Packages
MAC/OSX — ~/Library/Application Support/Sublime Text 3/Packages

"""

class GenerateUmlCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Get the currently selected line or lines
        line = self.view.line(self.view.sel()[0])
        text = self.view.substr(line)

        print(edit)

        # Create tokens from the text
        lexer = Lexer(text)

        # Interpret the tokens and create a diagram object
        # TODO need to handle InterpreterException thrown here
        interpreter = Interpreter(lexer)
        diagram = interpreter.evaluate()

        # Encode diagram for output to the view
        encoder = PrettyPrintEncoder()
        result = encoder.generate(diagram)

        # Replace selection
        self.view.replace(edit, line, result)

        contents = "new-content"

        # Send command to window
        self.view.window().run_command("create_new_file", 
                                      {"file_contents" : contents})


class CreateNewFileCommand(sublime_plugin.WindowCommand):
    def run(self, file_contents):
        self.file_contents = file_contents
        self.window.show_input_panel("Create class file?", "", 
                                    self.on_done, 
                                    None, 
                                    None)

    def on_done(self, text):
        view = self.window.new_file()
        view.run_command("add_text_to_new_file", {"text": self.file_contents})


class AddTextToNewFileCommand(sublime_plugin.TextCommand):
    def run(self, edit, text):
        self.view.insert(edit, 0, text)




import sublime
import sublime_plugin

from prexel.parser.lexer import Lexer
from prexel.parser.interpreter import Interpreter
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

        # Pretty-print encode diagram for output to the view
        pretty_print = PrettyPrintEncoder()
        result = pretty_print.generate(diagram)

        # Source-code encode diagram for files
        source_code = SourceCodeEncoder()
        classes = source_code.generate(diagram)

        # Replace selection
        self.view.replace(edit, line, result)

        # Send command to window
        self.view.window().run_command("create_new_file", 
                                      {"classes" : classes})


class CreateNewFileCommand(sublime_plugin.WindowCommand):
    def run(self, classes):
        self.classes = classes
        self.window.show_input_panel("Create class files? (YES or NO):", "", 
                                    self.on_done, 
                                    None, 
                                    None)

    def on_done(self, text):
        if text.lower().strip() in ("yes", "y"):
            for class_item in self.classes:
                print(class_item)
                file_name, file_contents = class_item
                view = self.window.new_file()
                view.run_command("add_text_to_new_file", 
                    {"file_name": file_name, "file_contents": file_contents})


class AddTextToNewFileCommand(sublime_plugin.TextCommand):
    def run(self, edit, file_name, file_contents):
        self.view.insert(edit, 0, file_contents)
        self.view.set_name(file_name + ".py")
        self.view.run_command('save')




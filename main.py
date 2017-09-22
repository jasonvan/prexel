import sublime
import sublime_plugin

from prexel.parser.lexer import Lexer
from prexel.parser.interpreter import Interpreter, InterpreterException
from prexel.encoders.pretty_print_encoder import PrettyPrintEncoder
from prexel.encoders.source_code_encoder import SourceCodeEncoder
from prexel.utils import Persistence


class GenerateUmlCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Get the currently selected line or lines
        line = self.view.line(self.view.sel()[0])
        easy_entry = self.view.substr(line)

        # Create tokens from the text
        lexer = Lexer(easy_entry)

        # Interpret the tokens and create a diagram object
        try:
            interpreter = Interpreter(lexer)
            diagram = interpreter.evaluate()
        except InterpreterException as e:
            self.view.show_popup("Invalid PREXEL syntax - {}".format(e),
                                 sublime.HIDE_ON_MOUSE_MOVE_AWAY)
            return

        # TODO display popup menu to determine if code should be created
        # self.view.show_popup_menu(["Create class(es)", "Don't create class(es)"], None)

        # Pretty-print encode diagram for output to the view
        pretty_print_encoder = PrettyPrintEncoder()
        pretty_print = pretty_print_encoder.generate(diagram)

        # Persist pretty_print, easy_entry values so we can reverse back to easy_entry
        persistence = Persistence()
        persistence.save(easy_entry, pretty_print)

        # Source-code encode diagram for files
        source_code = SourceCodeEncoder()
        classes = source_code.generate(diagram)

        # Replace selection
        self.view.replace(edit, line, pretty_print)

        # Send command to window
        self.view.window().run_command("create_new_file",
                                      {"classes": classes})


class ReverseUmlCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Get the currently selected line or lines
        line = self.view.line(self.view.sel()[0])
        pretty_print = self.view.substr(line)

        persistence = Persistence()
        easy_entry = persistence.load(pretty_print)

        # Replace selection
        if easy_entry:
            self.view.replace(edit, line, easy_entry)
        else:
            self.view.show_popup("Original string not found based on the current diagram.",
                                 sublime.HIDE_ON_MOUSE_MOVE_AWAY)


class CreateNewFileCommand(sublime_plugin.WindowCommand):
    def run(self, classes):
        self.classes = classes
        self.window.show_input_panel("Create class files? (YES or NO):", "",
                                     self.on_done, None, None)

    def on_done(self, text):
        if text.lower().strip() in ("yes", "y"):
            for class_item in self.classes:
                file_name, file_contents = class_item
                view = self.window.new_file()
                view.run_command("add_text_to_new_file",
                    {"file_name": file_name, "file_contents": file_contents})


class AddTextToNewFileCommand(sublime_plugin.TextCommand):
    def run(self, edit, file_name, file_contents):
        self.view.insert(edit, 0, file_contents)
        self.view.set_name(file_name + ".py")
        self.view.run_command('save')




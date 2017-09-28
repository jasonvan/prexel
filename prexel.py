import sublime
import sublime_plugin

from prexel.parser.lexer import Lexer
from prexel.parser.interpreter import Interpreter, InterpreterException
from prexel.encoders.pretty_print_encoder import PrettyPrintEncoder
from prexel.encoders.source_code_encoder import SourceCodeEncoder
from prexel.utils import Persistence, PrettyPrintStack

# Used to store the commands so they can be undone
pretty_print_stack = PrettyPrintStack()

class GenerateUmlCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Get the current selection or the line where the cursor is
        line = self.view.line(self.view.sel()[0])
        easy_entry = self.view.substr(line)

        # Parse and interpret the tokens and create a diagram object
        try:
            lexer = Lexer(easy_entry)
            interpreter = Interpreter(lexer)
            diagram = interpreter.evaluate()
        except InterpreterException as e:
            self.view.show_popup("Invalid PREXEL syntax - {}".format(e),
                                 sublime.HIDE_ON_MOUSE_MOVE_AWAY)
        else:
            # Cache some values that are needed by other methods
            self.edit = edit
            self.diagram = diagram
            self.easy_entry = easy_entry
            self.line = line

            # Show popup menu to determine what to generate
            self.view.show_popup_menu([
                "Generate UML",
                "Generate Source",
                "Generate Both UML and Source"
            ], self.on_done)

    def on_done(self, index):
        pretty_print = PrettyPrintEncoder().generate(self.diagram)
        source_code = SourceCodeEncoder().generate(self.diagram)

        if index == 0:
            self.output_pretty_print(pretty_print)
        elif index == 1:
            self.create_files(source_code)
        elif index == 2:
            self.output_pretty_print(pretty_print)
            self.create_files(source_code)

    def output_pretty_print(self, pretty_print):
        # Save the easy_entry string for recall later
        Persistence().save(self.easy_entry, pretty_print)

        # Push the last pretty_print value on stack, so we can undo if needed
        pretty_print_stack.push(pretty_print)

        # Replace easy-entry with pretty-print
        self.view.replace(self.edit, self.line, pretty_print)

    def create_files(self, source_code):
        # Call the CreateNewFileCommand object, sending the source code
        self.view.window().run_command("create_new_file",
                                      {"source_code": source_code})


class UndoUmlCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if not pretty_print_stack.is_empty():
            last_pretty_print = pretty_print_stack.peek()

            # persistence = Persistence()
            easy_entry = Persistence().load(last_pretty_print)

            # Replace selection
            if easy_entry:
                region = self.view.find(last_pretty_print, 0, sublime.LITERAL)
                self.view.replace(edit, region, easy_entry)
                pretty_print_stack.pop()
            else:
                errorMessage = "Original string not found based on the current diagram."
                self.view.show_popup(errorMessage,
                                     sublime.HIDE_ON_MOUSE_MOVE_AWAY)


class ReverseUmlCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Get the currently selected line or lines
        line = self.view.line(self.view.sel()[0])
        pretty_print = self.view.substr(line)

        # Check the prexel history for current selection
        persistence = Persistence()
        easy_entry = persistence.load(pretty_print)

        # Replace selection
        if easy_entry:
            self.view.replace(edit, line, easy_entry)
        else:
            errorMessage = "Original string not found based on the current diagram."
            self.view.show_popup(errorMessage,
                                 sublime.HIDE_ON_MOUSE_MOVE_AWAY)


class CreateNewFileCommand(sublime_plugin.WindowCommand):
    def run(self, source_code):
        for file in source_code:
            file_name, file_contents = file
            view = self.window.new_file()
            view.run_command("add_text_to_new_file",
                {"file_name": file_name, "file_contents": file_contents})


class AddTextToNewFileCommand(sublime_plugin.TextCommand):
    def run(self, edit, file_name, file_contents):
        self.view.insert(edit, 0, file_contents)
        self.view.set_name(file_name + ".py")
        self.view.run_command('save')




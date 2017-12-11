import sublime
import sublime_plugin

from prexel.parser.lexer import Lexer
from prexel.parser.interpreter import Interpreter, InterpreterException
from prexel.encoders.pretty_print_encoder import PrettyPrintEncoder
from prexel.encoders.source_code_encoder import SourceCodeEncoder
from prexel.encoders.xmi_encoder import XMIEncoder
from prexel.utils import Persistence, PrettyPrintStack

"""
Used to store the commands so they can be undone
 ________________ 
|PrettyPrintStack|
|----------------|
|stack           |
|push()          |
|pop()           |
|peek()          |
|is_empty()      |
|________________|

"""
pretty_print_stack = PrettyPrintStack()


class GenerateUmlCommand(sublime_plugin.TextCommand):
    """
    Main Command that generates UML and sources code
     __________________ 
    |GenerateUmlCommand|
    |------------------|
    |edit              |
    |diagram           |
    |easy_entry        |
    |line              |
    |run()             |
    |__________________|

    """
    def run(self, edit):
        # Get the current selection or the line where the cursor is
        line = self.view.line(self.view.sel()[0])
        easy_entry = self.view.substr(line)

        # Parse and interpret the tokens and create a diagram object
        try:
            full_diagram = None

            for item in easy_entry.split("\n\n"):
                if item:
                    lexer = Lexer(item)
                    interpreter = Interpreter(lexer)
                    current_diagram = interpreter.evaluate()

                    if full_diagram:
                        full_diagram.merge(current_diagram)
                    else:
                        full_diagram = current_diagram

        except InterpreterException as e:
            self.view.show_popup("Invalid PREXEL syntax - {}".format(e),
                                 sublime.HIDE_ON_MOUSE_MOVE_AWAY)
        else:
            # Cache some values that are needed by other methods
            self.diagram = full_diagram
            self.easy_entry = easy_entry
            self.line = line

            # Show popup menu to determine what to generate
            self.view.show_popup_menu([
                "Generate UML",
                "Generate Source",
                "Generate Both UML and Source"
            ], self.on_done)

    def on_done(self, index):
        # TODO - uncomment this
        # pretty_print = PrettyPrintEncoder().generate(self.diagram)
        source_code = SourceCodeEncoder().generate(self.diagram)
        # TODO - uncomment this
        # xmi = XMIEncoder().generate(self.diagram)

        if index == 0:
            # TODO - uncomment this
            # self.output_pretty_print(pretty_print)
            pass
        elif index == 1:
            self.create_files(source_code)
        elif index == 2:
            pass
            # TODO - uncomment this
            # self.output_pretty_print(pretty_print)
            # self.create_files(source_code)

        # TODO - uncomment this
        # xmi_files = ("sample-1", xmi)
        # self.create_files([xmi_files], ".xmi")

    def output_pretty_print(self, pretty_print):
        # Run new text command to replace the selection with pretty print
        self.view.window().run_command("output_pretty_print", {
            "easy_entry": self.easy_entry,
            "line": [self.line.begin(), self.line.end()],
            "pretty_print": pretty_print
        })

    def create_files(self, source_code, extension=".py"):
        # Call the CreateNewFileCommand object, sending the source code
        self.view.window().run_command(
            "create_new_file",
            {
                "source_code": source_code,
                "extension": extension
            }
        )


class OutputPrettyPrintCommand(sublime_plugin.TextCommand):
    def run(self, edit, easy_entry, line, pretty_print):
        # Cache the original easy entry string so it can
        # be recalled later.
        Persistence().save(easy_entry, pretty_print)

        # Push the last pretty_print value on stack, so we can undo if needed
        pretty_print_stack.push(pretty_print)

        # Create a Region object for the current selection
        region = sublime.Region(line[0], line[1])

        # Replace easy-entry with pretty-print
        self.view.replace(edit, region, pretty_print)


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
    def run(self, source_code, extension):
        for file in source_code:
            file_name, file_contents = file
            view = self.window.new_file()
            view.run_command(
                "add_text_to_new_file",
                {
                    "file_name": file_name, 
                    "file_contents": file_contents,
                    "extension": extension
                }
            )


class AddTextToNewFileCommand(sublime_plugin.TextCommand):
    def run(self, edit, file_name, file_contents, extension):
        self.view.insert(edit, 0, file_contents)
        self.view.set_name(file_name + extension)
        self.view.run_command('save')




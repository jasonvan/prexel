import sublime
import sublime_plugin
import re

# self.view.replace(edit, full_region, sample)


class GenerateUmlCommand(sublime_plugin.TextCommand):
    """
    TODO docstring
    """
    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                region_text = self.view.substr(region)
                prog = re.compile("[\n]{2,}")
                for element in prog.split(region_text):
                    """
                    TODO:
                    1) Need to match the class marker
                    2) Need to match methods
                    """
                    print("Element")
                    print(element)

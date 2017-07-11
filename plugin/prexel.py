import sublime
import sublime_plugin
import re

# self.view.replace(edit, full_region, sample)

capital_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# TODO review these regex
prog = re.compile("[\n]{2,}")
class_marker = re.compile("^[|](?![|])")


class GenerateUmlCommand(sublime_plugin.TextCommand):
    """
    TODO docstring
    """
    def run(self, edit):
        # TODO comment code below
        for region in self.view.sel():
            if not region.empty():
                region_text = self.view.substr(region)
                for element in prog.split(region_text):
                    class_name = ""
                    methods = []
                    for line in element.splitlines():
                        if class_marker.match(line):
                            line = re.sub(class_marker, "", line)
                            if not class_name and line[0] in capital_letters:
                                class_name = line
                            elif line[-2:] == "()":
                                methods.append(line[:-2])

                    print(class_name)
                    print(methods)

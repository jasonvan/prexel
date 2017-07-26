import sublime
import sublime_plugin
import re


class GenerateUmlCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                region_text = self.view.substr(region)
                # TODO Do string processing here

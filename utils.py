import hashlib
import os

PLUGIN_DIR = os.path.dirname(os.path.realpath(__file__))


class Persistence:
    """
    TODO
    - Add comments to this class and test class
    - Try to optimize the hashcode search
    """
    def __init__(self, filename=".prexel-history"):
        self.filename = filename

    def save(self, easy_entry, pretty_printed):
        hashcode = self._generate_hashcode(pretty_printed)
        self._save_easy_entry(hashcode, easy_entry)

    def load(self, pretty_printed):
        hashcode = self._generate_hashcode(pretty_printed)
        return self._load_easy_entry(hashcode)

    def _save_easy_entry(self, hashcode, easy_entry_value):
        # Check if easy_entry string already exists in history file
        easy_entry = self._load_easy_entry(hashcode)

        if not easy_entry:
            easy_entry_value = easy_entry_value.replace("\n", "[!NL]")
            with open(self.history_file_path(), "a") as file:
                file.write("{}:{}\n".format(hashcode, easy_entry_value))

    def _load_easy_entry(self, hashcode):
        easy_entry = None

        try:
            with open(self.history_file_path()) as file:
                for line in file:
                    if hashcode in line:
                        easy_entry = line.split(":")[1].strip().replace("[!NL]", "\n")
        except FileNotFoundError:
            pass  # TODO handle error

        return easy_entry

    def history_file_path(self):
        return os.path.join(PLUGIN_DIR, self.filename)

    @staticmethod
    def _generate_hashcode(pretty_printed_value):
        return hashlib.md5(pretty_printed_value.strip().encode('utf-8')).hexdigest()

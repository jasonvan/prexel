import unittest
import os
from prexel.utils import Persistence

PLUGIN_DIR = os.path.dirname(os.path.realpath(__file__))
HISTORY_FILE = os.path.join(PLUGIN_DIR, ".test-history")


class TestUtilsPersistence(unittest.TestCase):
    def setUp(self):
        self.persistence = Persistence(".test-history")

    def tearDown(self):
        try:
            os.remove(self.persistence.history_file_path())
        except FileNotFoundError:
            pass  # Don't need to do anything

    def test_generate_hashcode_pretty_print(self):
        pretty_print = """
 ____ 
|Room|
|____|
∆
|_______ 
|Kitchen|
|_______|
        """

        self.assertEqual("8348e2327ecaa4d3370be6dd635e31e1",
                         self.persistence._generate_hashcode(pretty_print))

    def test_generate_hashcode_pretty_print_with_whitespace(self):
        pretty_print = """
     ____ 
    |Room|
    |____|
    ∆
    |_______ 
    |Kitchen|
    |_______|
        """

        self.assertEqual("8348e2327ecaa4d3370be6dd635e31e1",
                         self.persistence._generate_hashcode(pretty_print))

    def test_save_pretty_printed(self):
        hashcode = "23isajkf02"
        easy_entry = "|Room >> Kitchen"
        self.persistence._save_easy_entry(hashcode, easy_entry)

        history_file = self.persistence.history_file_path()

        with open(history_file) as file:
            from_history_file = file.readline()

        self.assertEqual("23isajkf02:|Room >> Kitchen\n", from_history_file)

    def test_save_pretty_printed_includes_newline(self):
        hashcode = "23isajkf02"
        easy_entry = "|Room >> Kitchen\n|field1\n|field2"
        self.persistence._save_easy_entry(hashcode, easy_entry)

        history_file = self.persistence.history_file_path()

        with open(history_file) as file:
            from_history_file = file.readline()

        self.assertEqual("23isajkf02:|Room >> Kitchen[!NL]|field1[!NL]|field2\n", from_history_file)

    def test_save_pretty_printed_already_exists(self):
        hashcode = "23isajkf02"
        easy_entry = "|Room >> Kitchen"
        self.persistence._save_easy_entry(hashcode, easy_entry)
        self.persistence._save_easy_entry(hashcode, easy_entry)

        history_file = self.persistence.history_file_path()

        with open(history_file) as file:
            from_history_file = file.readlines()

        self.assertEqual("23isajkf02:|Room >> Kitchen\n", "".join(from_history_file))

    def test_load_easy_entry(self):
        hashcode = "23isajkf02"
        easy_entry = "|Room >> Kitchen"

        self.persistence._save_easy_entry(hashcode, easy_entry)
        self.assertEqual(easy_entry, self.persistence._load_easy_entry(hashcode))

    def test_load_easy_entry_includes_newline(self):
        hashcode = "23isajkf02"
        easy_entry = "|Room >> Kitchen\n|field1\n|field2"
        self.persistence._save_easy_entry(hashcode, easy_entry)
        self.assertEqual(easy_entry, self.persistence._load_easy_entry(hashcode))


if __name__ == '__main__':
    unittest.main()

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

    def test_generate_hashcode_simple(self):
        self.assertEqual("b10a8db164e0754105b7a99be72e3fe5",
                         self.persistence._generate_hashcode("Hello World"))

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

        self.assertEqual("38214b075b76fa0d66b439042fbd9e4d",
                         self.persistence._generate_hashcode(pretty_print))

    def test_save_pretty_printed(self):
        hashcode = "23isajkf02"
        easy_entry = "|Room >> Kitchen"
        self.persistence._save_pretty_printed(hashcode, easy_entry)

        history_file = self.persistence.history_file_path()

        with open(history_file) as file:
            from_history_file = file.readline()

        self.assertEqual("23isajkf02:|Room >> Kitchen\n", from_history_file)

    def test_save_pretty_printed_already_exists(self):
        hashcode = "23isajkf02"
        easy_entry = "|Room >> Kitchen"
        self.persistence._save_pretty_printed(hashcode, easy_entry)
        self.persistence._save_pretty_printed(hashcode, easy_entry)

        history_file = self.persistence.history_file_path()

        with open(history_file) as file:
            from_history_file = file.readlines()

        self.assertEqual("23isajkf02:|Room >> Kitchen\n", "".join(from_history_file))

    def test_load_easy_entry(self):
        hashcode = "23isajkf02"
        easy_entry = "|Room >> Kitchen"

        self.persistence._save_pretty_printed(hashcode, easy_entry)
        self.assertEqual(easy_entry, self.persistence._load_easy_entry(hashcode))


if __name__ == '__main__':
    unittest.main()

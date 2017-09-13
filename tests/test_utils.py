import unittest
from prexel import utils


class TestUtils(unittest.TestCase):

    def test_generate_hashcode(self):
        self.assertEqual("b10a8db164e0754105b7a99be72e3fe5",
                         utils.generate_hashcode("Hello World"))


if __name__ == '__main__':
    unittest.main()

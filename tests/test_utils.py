import unittest
from prexel import utils


class TestUtils(unittest.TestCase):

    def test_generate_hashcode(self):
        self.assertEqual("b10a8db164e0754105b7a99be72e3fe5",
                         utils.generate_hashcode("Hello World"))

        prexel = """
 ____ 
|Room|
|____|
∆
|_______ 
|Kitchen|
|_______|
        """

        self.assertEqual("38214b075b76fa0d66b439042fbd9e4d",
                         utils.generate_hashcode(prexel))

    def test_save_pretty_printed(self):
        prexel = """
 ____ 
|Room|
|____|
∆
|_______ 
|Kitchen|
|_______|
        """
        hashcode = utils.generate_hashcode(prexel)
        utils.save_pretty_printed(hashcode, "|Room >> Kitchen", ".history-test")


if __name__ == '__main__':
    unittest.main()

import unittest
from prexel.plugin import REGEX


class TestRegex(unittest.TestCase):
    def test_class_name_regex(self):
        class_name_regex = REGEX["class_name"]

        # These should match
        self.assertTrue(class_name_regex.match("Kitchen"))
        self.assertTrue(class_name_regex.match("Wing"))
        self.assertTrue(class_name_regex.match("Style"))
        self.assertTrue(class_name_regex.match("A"))

        # These shouldn't match
        self.assertFalse(class_name_regex.match("$Class"))
        self.assertFalse(class_name_regex.match("kitchen"))
        self.assertFalse(class_name_regex.match("Kitchen()"))
        self.assertFalse(class_name_regex.match("method()"))

    def test_method_signature_regex(self):
        method_signature_regex = REGEX["method_signature"]

        # These should match
        self.assertTrue(method_signature_regex.match("sample_method()"))
        self.assertTrue(method_signature_regex.match("sample_method(param1,[])"))

        # These shouldn't match
        self.assertFalse(method_signature_regex.match("sample_method"))
        self.assertFalse(method_signature_regex.match("Sample_method"))
        self.assertFalse(method_signature_regex.match("()"))

    def test_aggregation_regex(self):
        aggregation_regex = REGEX["aggregation"]

        # These should match
        self.assertTrue(aggregation_regex.match("<>-->"))
        self.assertTrue(aggregation_regex.match("<>-------->"))
        self.assertTrue(aggregation_regex.match("<>1-->"))
        self.assertTrue(aggregation_regex.match("<>*-->"))
        self.assertTrue(aggregation_regex.match("<>1--*>"))
        self.assertTrue(aggregation_regex.match("<>1--1>"))
        self.assertTrue(aggregation_regex.match("<>*--1>"))
        self.assertTrue(aggregation_regex.match("<>*--*>"))
        self.assertTrue(aggregation_regex.match("<>*-name-*>"))
        self.assertTrue(aggregation_regex.match("<>--name--->"))

        # These shouldn't match
        self.assertFalse(aggregation_regex.match("<>--"))
        self.assertFalse(aggregation_regex.match("-->"))
        self.assertFalse(aggregation_regex.match("<>&-->"))
        self.assertFalse(aggregation_regex.match("<>--&>"))
        self.assertFalse(aggregation_regex.match("<>1a--1b>"))

if __name__ == '__main__':
    unittest.main()
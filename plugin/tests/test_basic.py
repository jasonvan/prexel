import unittest
from prexel.plugin.encoders import PrettyPrintEncoder, SourceCodeEncoder


class TestPrettyPrintEncoder(unittest.TestCase):
    def test_generate_class_header(self):
        encoder = PrettyPrintEncoder()
        expected = """
 _____________________ 
|       Kitchen       |
|---------------------|
"""
        actual = encoder.generate_class_header(21, "Kitchen")
        self.assertEqual(actual, expected)

    def test_generate_class_body(self):
        encoder = PrettyPrintEncoder()
        expected = """|arrange_kitchen()    |
|place_floor_cabinet()|
|place_wall_cabinet() |
 --------------------- 
"""
        methods = [
            "arrange_kitchen()",
            "place_floor_cabinet()",
            "place_wall_cabinet()"
        ]

        fields = []
        actual = encoder.generate_class_body(21, methods, fields)

        self.assertEqual(actual, expected)

    def test_generate_class(self):
        diagram_element = {
            "name":"Kitchen",
            "type":"class",
            "methods": [
                "arrange_kitchen()",
                "place_floor_cabinet()",
                "place_wall_cabinet()"
            ],
        }

        expected = """
 _____________________ 
|       Kitchen       |
|---------------------|
|arrange_kitchen()    |
|place_floor_cabinet()|
|place_wall_cabinet() |
 --------------------- 
"""
        encoder = PrettyPrintEncoder()
        actual = encoder.generate_class(diagram_element)

        self.assertEqual(expected, actual)


class TestSourceCodeEncoder(unittest.TestCase):
    def test_generate_class(self):
        diagram_element = {
            "name":"Kitchen",
            "type":"class",
            "fields": [
                "width",
                "height"
            ],
            "methods": [
                "arrange_kitchen()",
                "place_floor_cabinet()",
                "place_wall_cabinet()"
            ],
        }

        expected = """class Kitchen:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def arrange_kitchen(self):
        pass

    def place_floor_cabinet(self):
        pass

    def place_wall_cabinet(self):
        pass
"""

        encoder = SourceCodeEncoder()
        actual = encoder.generate_class(diagram_element)

        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()

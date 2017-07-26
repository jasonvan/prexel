import unittest

from prexel.plugin.encoders.pretty_print_encoder import PrettyPrintEncoder
from prexel.plugin.models.diagram import Diagram


class TestPrettyPrintEncoder(unittest.TestCase):
    def test_generate_class_header(self):
        expected = (" _____________________ \n"
                    "|       Kitchen       |\n"
                    "|---------------------|\n")

        encoder = PrettyPrintEncoder()
        actual = encoder.generate_class_header(21, "Kitchen")

        self.assertEqual(actual, expected)

    def test_generate_class_body(self):
        expected = ("|arrange_kitchen()    |\n"
                    "|place_floor_cabinet()|\n"
                    "|place_wall_cabinet() |\n"
                    "|_____________________|\n")

        diagram = Diagram("Kitchen", methods=[
            "arrange_kitchen()",
            "place_floor_cabinet()",
            "place_wall_cabinet()"
        ])

        encoder = PrettyPrintEncoder()
        actual = encoder.generate_class_body(21, diagram)

        self.assertEqual(actual, expected)

    def test_generate_class(self):
        diagram = Diagram("Kitchen", methods=[
            "arrange_kitchen()",
            "place_floor_cabinet()",
            "place_wall_cabinet()"
        ])

        expected = (" _____________________ \n"
                    "|       Kitchen       |\n"
                    "|---------------------|\n"
                    "|arrange_kitchen()    |\n"
                    "|place_floor_cabinet()|\n"
                    "|place_wall_cabinet() |\n"
                    "|_____________________|\n")

        encoder = PrettyPrintEncoder()
        actual = encoder.generate_class(diagram)

        self.assertEqual(expected, actual)

    def test_generate_class_with_inheritance(self):
        pass  # TODO implement


if __name__ == '__main__':
    unittest.main()

import unittest

from prexel.plugin.encoders.pretty_print_encoder import PrettyPrintEncoder
from prexel.plugin.models.diagram import ClassDiagram, InheritanceDiagram


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

        diagram = ClassDiagram("Kitchen", methods=[
            "arrange_kitchen()",
            "place_floor_cabinet()",
            "place_wall_cabinet()"
        ])

        encoder = PrettyPrintEncoder()
        actual = encoder.generate_class_body(21, diagram)

        self.assertEqual(actual, expected)

    def test_generate_class(self):
        diagram = ClassDiagram("Kitchen", methods=[
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

    def test_generate_empty_class(self):
        diagram = ClassDiagram("Kitchen")

        expected = (" _______ \n"
                    "|Kitchen|\n"
                    "|_______|\n")

        encoder = PrettyPrintEncoder()
        actual = encoder.generate_class(diagram)

        self.assertEqual(expected, actual)

    def test_generate_class_with_inheritance(self):
        room_diagram = ClassDiagram("Room")
        kitchen_diagram = ClassDiagram("Kitchen", methods=[
            "arrange_kitchen()",
            "place_floor_cabinet()",
            "place_wall_cabinet()"
        ], extends="Room")

        expected = (" ____ \n"
                    "|Room|\n"
                    "|____|\n"
                    "∆                      \n"
                    "|_____________________ \n"
                    "|       Kitchen       |\n"
                    "|---------------------|\n"
                    "|arrange_kitchen()    |\n"
                    "|place_floor_cabinet()|\n"
                    "|place_wall_cabinet() |\n"
                    "|_____________________|\n")

        encoder = PrettyPrintEncoder()

        kitchen_class = encoder.generate_class(kitchen_diagram)
        room_class = encoder.generate_class(room_diagram)
        actual = encoder.concat_results([room_class, kitchen_class])

        self.assertEqual(expected, actual)

    def test_generate_class_with_inheritance_advanced(self):
        room_diagram = ClassDiagram("Room", fields=[
            "width",
            "height"
        ], methods=[
            "set_color()"
        ])
        kitchen_diagram = ClassDiagram("Kitchen", methods=[
            "arrange_kitchen()",
            "place_floor_cabinet()",
            "place_wall_cabinet()"
        ], extends="Room")

        expected = (" ___________ \n"
                    "|   Room    |\n"
                    "|-----------|\n"
                    "|width      |\n"
                    "|height     |\n"
                    "|set_color()|\n"
                    "|___________|\n"
                    "∆                      \n"
                    "|_____________________ \n"
                    "|       Kitchen       |\n"
                    "|---------------------|\n"
                    "|arrange_kitchen()    |\n"
                    "|place_floor_cabinet()|\n"
                    "|place_wall_cabinet() |\n"
                    "|_____________________|\n")

        encoder = PrettyPrintEncoder()

        kitchen_class = encoder.generate_class(kitchen_diagram)
        room_class = encoder.generate_class(room_diagram)
        actual = encoder.concat_results([room_class, kitchen_class])

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()

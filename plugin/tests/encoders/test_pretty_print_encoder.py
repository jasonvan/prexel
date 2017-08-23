import unittest

from prexel.plugin.encoders.pretty_print_encoder import PrettyPrintEncoder
from prexel.plugin.models.diagram import (ClassDiagram,
                                          InheritanceDiagram,
                                          AggregationDiagram)


class TestPrettyPrintEncoder(unittest.TestCase):
    def test_generate_class_header(self):
        diagram = ClassDiagram("Kitchen", methods=[
            "arrange_kitchen()",
            "place_floor_cabinet()",
            "place_wall_cabinet()"
        ])

        expected = (" _____________________ \n"
                    "|       Kitchen       |\n"
                    "|---------------------|\n")

        max_length = 21
        encoder = PrettyPrintEncoder()
        actual = encoder.generate_class_header(max_length, diagram)

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

        max_length = 21
        encoder = PrettyPrintEncoder()
        actual = encoder.generate_class_body(max_length, diagram)

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

    def test_generate_aggregation(self):
        task_list_aggregation = AggregationDiagram("the_tasks",
                                                   right_multiplicity="*")

        expected = "<>-the_tasks---*>"

        encoder = PrettyPrintEncoder()
        actual = encoder.generate_aggregation(task_list_aggregation)

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

    def test_generate_class_with_aggregation(self):
        task_list_diagram = ClassDiagram("TaskList", methods=[
            "get_the_tasks()",
            "prioritize()"
        ])

        task_list_aggregation = AggregationDiagram("the_tasks",
                                                   right_multiplicity="*")

        task_diagram = ClassDiagram("Task")

        # 1. split diagrams on new line
        # 2. get the length of the aggregation
        # 3. determine the max height, max_length
        # 4. combine the matching values at each of the indexes
        # 5. join on \n
        # 6. append \n

        expected = (" ______________                   ____ \n"
                    "|   TaskList   |<>-the_tasks---*>|Task|\n"
                    "|--------------|                 |____|\n"
                    "|get_the_task()|\n"
                    "|prioritize()  |\n"
                    "|______________|\n")




if __name__ == '__main__':
    unittest.main()

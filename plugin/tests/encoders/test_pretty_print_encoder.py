import unittest

from prexel.plugin.encoders.pretty_print_encoder import PrettyPrintEncoder
from prexel.plugin.models.diagram import (ClassDiagramPart,
                                          InheritanceDiagramPart,
                                          AggregationDiagramPart)


class TestPrettyPrintEncoder(unittest.TestCase):
    def test_generate_class_header(self):
        diagram = ClassDiagramPart("Kitchen", methods=[
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

        diagram = ClassDiagramPart("Kitchen", methods=[
            "arrange_kitchen()",
            "place_floor_cabinet()",
            "place_wall_cabinet()"
        ])

        max_length = 21
        encoder = PrettyPrintEncoder()
        actual = encoder.generate_class_body(max_length, diagram)

        self.assertEqual(actual, expected)

    def test_generate_class(self):
        diagram = ClassDiagramPart("Kitchen", methods=[
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
        diagram = ClassDiagramPart("Kitchen")

        expected = (" _______ \n"
                    "|Kitchen|\n"
                    "|_______|\n")

        encoder = PrettyPrintEncoder()
        actual = encoder.generate_class(diagram)

        self.assertEqual(expected, actual)

    def test_generate_aggregation(self):
        task_list_aggregation = AggregationDiagramPart("the_tasks",
                                                       right_multiplicity="*")

        expected = "<>-the_tasks---*>"

        encoder = PrettyPrintEncoder()
        actual = encoder.generate_aggregation(task_list_aggregation)

        self.assertEqual(expected, actual)

    def test_generate_class_with_inheritance(self):
        room_diagram = ClassDiagramPart("Room")
        kitchen_diagram = ClassDiagramPart("Kitchen", methods=[
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
        actual = encoder.concat_inheritance(parent=room_class,
                                            children=[kitchen_class])

        self.assertEqual(expected, actual)

    def test_concat_inheritance(self):
        room_diagram = ClassDiagramPart("Room", fields=[
            "width",
            "height"
        ], methods=[
            "set_color()"
        ])

        kitchen_diagram = ClassDiagramPart("Kitchen", methods=[
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
        actual = encoder.concat_inheritance(parent=room_class,
                                            children=[kitchen_class])

        self.assertEqual(expected, actual)

    def test_concat_aggregation(self):
        task_list_diagram = ClassDiagramPart("TaskList", methods=[
            "get_the_tasks()",
            "prioritize()"
        ])

        task_list_aggregation = AggregationDiagramPart("the_tasks",
                                                       right_multiplicity="*")

        task_diagram = ClassDiagramPart("Task")

        expected = (" _______________                   ____ \n"
                    "|   TaskList    |<>-the_tasks---*>|Task|\n"
                    "|---------------|                 |____|\n"
                    "|get_the_tasks()|                       \n"
                    "|prioritize()   |                       \n"
                    "|_______________|                       \n")

        encoder = PrettyPrintEncoder()
        task_list = encoder.generate_class(task_list_diagram)
        aggregation = encoder.generate_aggregation(task_list_aggregation)
        task = encoder.generate_class(task_diagram)

        actual = encoder.concat_aggregation(aggregator=task_list,
                                            aggregation=aggregation,
                                            aggregated=task)

    def test_concat_aggregation_alt(self):
        task_list_diagram = ClassDiagramPart("TaskList", methods=[
            "get_the_tasks()",
            "prioritize()"
        ])

        task_list_aggregation = AggregationDiagramPart("the_tasks",
                                                       left_multiplicity="10",
                                                       right_multiplicity="*")

        task_diagram = ClassDiagramPart("Task", fields=[
            "field1",
            "field2",
            "field3"
        ], methods=[
            "method1()",
            "method2()",
            "method3()"
        ])

        expected = (" _______________                     _________ \n"
                    "|   TaskList    |<>10-the_tasks---*>|  Task   |\n"
                    "|---------------|                   |---------|\n"
                    "|get_the_tasks()|                   |field1   |\n"
                    "|prioritize()   |                   |field2   |\n"
                    "|_______________|                   |field3   |\n"
                    "                                    |method1()|\n"
                    "                                    |method2()|\n"
                    "                                    |method3()|\n"
                    "                                    |_________|\n")

        encoder = PrettyPrintEncoder()
        task_list = encoder.generate_class(task_list_diagram)
        aggregation = encoder.generate_aggregation(task_list_aggregation)
        task = encoder.generate_class(task_diagram)

        actual = encoder.concat_aggregation(aggregator=task_list,
                                            aggregation=aggregation,
                                            aggregated=task)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()

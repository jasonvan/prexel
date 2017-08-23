import unittest

from prexel.plugin.encoders.pretty_print_encoder import PrettyPrintEncoder
from prexel.plugin.models.diagram import (Diagram,
                                          ClassDiagramPart,
                                          InheritanceDiagramPart,
                                          AggregationDiagramPart)


class TestPrettyPrintEncoderMain(unittest.TestCase):
    """
    Tests related to main generate method
    """
    def test_generate_with_inheritance(self):
        room = ClassDiagramPart("Room")
        inheritance = InheritanceDiagramPart()
        kitchen = ClassDiagramPart("Kitchen", methods=[
            "arrange_kitchen()",
            "place_floor_cabinet()",
            "place_wall_cabinet()"
        ])

        diagram = Diagram(kitchen,
                          parent=room,
                          inheritance=inheritance)

        expected = (" ____ \n"
                    "|Room|\n"
                    "|____|\n"
                    "∆\n"
                    "|_____________________ \n"
                    "|       Kitchen       |\n"
                    "|---------------------|\n"
                    "|arrange_kitchen()    |\n"
                    "|place_floor_cabinet()|\n"
                    "|place_wall_cabinet() |\n"
                    "|_____________________|\n")

        encoder = PrettyPrintEncoder()
        actual = encoder.generate(diagram)
        self.assertEqual(expected, actual)

    def test_generate_with_inheritance_alt(self):
        room = ClassDiagramPart("Room", fields=[
            "width",
            "height"
        ], methods=[
            "set_color()"
        ])

        inheritance = InheritanceDiagramPart()

        kitchen = ClassDiagramPart("Kitchen", methods=[
            "arrange_kitchen()",
            "place_floor_cabinet()",
            "place_wall_cabinet()"
        ])

        diagram = Diagram(kitchen,
                          parent=room,
                          inheritance=inheritance)

        expected = (" ___________ \n"
                    "|   Room    |\n"
                    "|-----------|\n"
                    "|width      |\n"
                    "|height     |\n"
                    "|set_color()|\n"
                    "|___________|\n"
                    "∆\n"
                    "|_____________________ \n"
                    "|       Kitchen       |\n"
                    "|---------------------|\n"
                    "|arrange_kitchen()    |\n"
                    "|place_floor_cabinet()|\n"
                    "|place_wall_cabinet() |\n"
                    "|_____________________|\n")

        encoder = PrettyPrintEncoder()
        actual = encoder.generate(diagram)
        self.assertEqual(expected, actual)

    def test_generate_with_aggregation(self):
        task_list_diagram = ClassDiagramPart("TaskList", methods=[
            "get_the_tasks()",
            "prioritize()"
        ])

        task_list_aggregation = AggregationDiagramPart("the_tasks",
                                                       right_multiplicity="*")

        task_diagram = ClassDiagramPart("Task")

        diagram = Diagram(task_list_diagram,
                          aggregation=task_list_aggregation,
                          aggregated=task_diagram)

        expected = (" _______________                   ____ \n"
                    "|   TaskList    |<>-the_tasks---*>|Task|\n"
                    "|---------------|                 |____|\n"
                    "|get_the_tasks()|                       \n"
                    "|prioritize()   |                       \n"
                    "|_______________|                       \n")

        encoder = PrettyPrintEncoder()
        actual = encoder.generate(diagram)
        self.assertEqual(expected, actual)

    def test_generate_full(self):
        task_list_diagram = ClassDiagramPart("TaskList", methods=[
            "get_the_tasks()",
            "prioritize()"
        ])

        task_list_aggregation = AggregationDiagramPart("the_tasks",
                                                       right_multiplicity="*")

        task_diagram = ClassDiagramPart("Task", fields=[
            "name",
            "description"
        ])

        parent = ClassDiagramPart("Manager", fields=[
            "field1",
            "field2"
        ], methods=[
            "method1()",
            "method2()"
        ])

        inheritance = InheritanceDiagramPart()

        diagram = Diagram(task_list_diagram,
                          parent=parent,
                          inheritance=inheritance,
                          aggregation=task_list_aggregation,
                          aggregated=task_diagram)

        expected = (" _________ \n"
                    "| Manager |\n"
                    "|---------|\n"
                    "|field1   |\n"
                    "|field2   |\n"
                    "|method1()|\n"
                    "|method2()|\n"
                    "|_________|\n"
                    "∆\n"
                    "|_______________                   ___________ \n"
                    "|   TaskList    |<>-the_tasks---*>|   Task    |\n"
                    "|---------------|                 |-----------|\n"
                    "|get_the_tasks()|                 |name       |\n"
                    "|prioritize()   |                 |description|\n"
                    "|_______________|                 |___________|\n")

        encoder = PrettyPrintEncoder()
        actual = encoder.generate(diagram)
        self.assertEqual(expected, actual)


class TestPrettyPrintEncoderHelpers(unittest.TestCase):
    """
    Helper tests
    """
    def test_create_class(self):
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
        actual = encoder.create_class(diagram)

        self.assertEqual(expected, actual)

    def test_create_class_empty(self):
        diagram = ClassDiagramPart("Kitchen")

        expected = (" _______ \n"
                    "|Kitchen|\n"
                    "|_______|\n")

        encoder = PrettyPrintEncoder()
        actual = encoder.create_class(diagram)

        self.assertEqual(expected, actual)

    def test_create_aggregation_arrow(self):
        task_list_aggregation = AggregationDiagramPart("the_tasks",
                                                       right_multiplicity="*")

        expected = "<>-the_tasks---*>"

        encoder = PrettyPrintEncoder()
        actual = encoder.create_aggregation_arrow(task_list_aggregation)

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
        task_list = encoder.create_class(task_list_diagram)
        aggregation = encoder.create_aggregation_arrow(task_list_aggregation)
        task = encoder.create_class(task_diagram)

        actual = encoder.concat_aggregation(aggregator=task_list,
                                            aggregation=aggregation,
                                            aggregated=task)

        self.assertEqual(expected, actual)

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
        task_list = encoder.create_class(task_list_diagram)
        aggregation = encoder.create_aggregation_arrow(task_list_aggregation)
        task = encoder.create_class(task_diagram)

        actual = encoder.concat_aggregation(aggregator=task_list,
                                            aggregation=aggregation,
                                            aggregated=task)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()

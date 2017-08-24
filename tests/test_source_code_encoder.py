import unittest

from prexel.encoders.source_code_encoder import SourceCodeEncoder
from prexel.models.diagram import (Diagram,
                                   ClassDiagramPart,
                                   InheritanceDiagramPart,
                                   AggregationDiagramPart)


class TestSourceCodeEncoderMain(unittest.TestCase):
    """
    Tests related to main generate method
    """
    def test_generate_empty_class(self):
        wing = ClassDiagramPart("Wing")

        diagram = Diagram(wing)

        expected = ("class Wing:\n"
                    "    pass\n")

        encoder = SourceCodeEncoder()
        actual = encoder.generate(diagram)

        self.assertEqual("wing", actual[0][0])
        self.assertEqual(expected, actual[0][1])

    def test_generate_with_inheritance(self):
        person = ClassDiagramPart("Person", fields=[
            "name",
            "age"
        ])

        inheritance = InheritanceDiagramPart()

        employee = ClassDiagramPart("Employee", fields=[
            "job_title"
        ])

        diagram = Diagram(employee,
                          parent=person,
                          inheritance=inheritance)

        # TODO Employee should contain call to super().__init__() with value

        person_class = ("class Person:\n"
                        "    def __init__(self, name, age):\n"
                        "        self.name = name\n"
                        "        self.age = age\n")

        employee_class = ("class Employee(Person):\n"
                          "    def __init__(self, job_title):\n"
                          "        self.job_title = job_title\n")

        encoder = SourceCodeEncoder()
        actual = encoder.generate(diagram)  # Returns and array of classes

        self.assertEqual("person", actual[0][0])
        self.assertEqual(person_class, actual[0][1])
        self.assertEqual("employee", actual[1][0])
        self.assertEqual(employee_class, actual[1][1])

    def test_generate_with_aggregation(self):
        task_list_diagram = ClassDiagramPart("TaskList", methods=[
            "get_the_tasks()",
            "prioritize()"
        ], fields=["the_tasks"])

        task_list_aggregation = AggregationDiagramPart("the_tasks",
                                                       right_multiplicity="*")

        task_diagram = ClassDiagramPart("Task")

        diagram = Diagram(task_list_diagram,
                          aggregation=task_list_aggregation,
                          aggregated=task_diagram)

        task_list_class = ("class TaskList:\n"
                           "    def __init__(self, the_tasks):\n"
                           "        self.the_tasks = the_tasks\n"
                           "\n"
                           "    def get_the_tasks(self):\n"
                           "        pass\n"
                           "\n"
                           "    def prioritize(self):\n"
                           "        pass\n")

        task_class = ("class Task:\n"
                      "    pass\n")

        encoder = SourceCodeEncoder()
        actual = encoder.generate(diagram)

        self.assertEqual("tasklist", actual[1][0])
        self.assertEqual(task_list_class, actual[1][1])
        self.assertEqual("task", actual[0][0])
        self.assertEqual(task_class, actual[0][1])

    def test_generate_full(self):
        task_list_diagram = ClassDiagramPart("TaskList", methods=[
            "get_the_tasks()",
            "prioritize()"
        ])

        task_list_aggregation = AggregationDiagramPart("name",
                                                       right_multiplicity="*")

        task_diagram = ClassDiagramPart("Task", fields=[
            "name",
            "description"
        ], methods=[
            "complete()",
            "delete()"
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

        encoder = SourceCodeEncoder()
        actual = encoder.generate(diagram)

        # NOT TESTING ANYTHING, JUST CHECKING OUTPUT
        print(actual[0][1])
        print(actual[1][1])
        print(actual[2][2])


class TestSourceCodeEncoderMainHelpers(unittest.TestCase):
    """
    Helper tests
    """
    def test_create_class(self):
        diagram = ClassDiagramPart("Kitchen", methods=[
            "arrange_kitchen()",
            "place_floor_cabinet()",
            "place_wall_cabinet()"
        ], fields=[
            "width",
            "height"
        ])

        expected = ("class Kitchen:\n"
                    "    def __init__(self, width, height):\n"
                    "        self.width = width\n"
                    "        self.height = height\n"
                    "\n"
                    "    def arrange_kitchen(self):\n"
                    "        pass\n"
                    "\n"
                    "    def place_floor_cabinet(self):\n"
                    "        pass\n"
                    "\n"
                    "    def place_wall_cabinet(self):\n"
                    "        pass\n"
                    )

        encoder = SourceCodeEncoder()
        actual = encoder.create_class(diagram)

        self.assertEqual(expected, actual)

    def test_generate_class_with_method_params_as_object(self):
        style_diagram = ClassDiagramPart("Style", methods=[
            {"signature": "get_cabinet(height)", "body": "return XCabinet()"}
        ])

        xcabinet_diagram = ClassDiagramPart("XCabinet")

        expected = ("class Style:\n"
                    "    def get_cabinet(self, height):\n"
                    "        return XCabinet()\n"
                    "class XCabinet:\n"
                    "    pass\n"
                    )

        encoder = SourceCodeEncoder()
        style = encoder.create_class(style_diagram)
        xcabinet = encoder.create_class(xcabinet_diagram)

        actual = style + xcabinet

        self.assertEqual(expected, actual)

    def test_generate_class_with_method_params(self):
        diagram = ClassDiagramPart("MyClass", methods=[
            "crazy_method2Name(param1, param2)"
        ])

        expected = ("class MyClass:\n"
                    "    def crazy_method2Name(self, param1, param2):\n"
                    "        pass\n")

        encoder = SourceCodeEncoder()
        actual = encoder.create_class(diagram)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()

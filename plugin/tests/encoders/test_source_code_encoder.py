import unittest

from prexel.plugin.encoders.source_code_encoder import SourceCodeEncoder
from prexel.plugin.models.diagram import Diagram


class TestSourceCodeEncoder(unittest.TestCase):
    def test_generate_class(self):
        diagram = Diagram("Kitchen", methods=[
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
                    "\n"
                    )

        encoder = SourceCodeEncoder()
        actual = encoder.generate_class(diagram)

        self.assertEqual(expected, actual)

    def test_generate_class_with_inheritance(self):
        person_diagram = Diagram("Person", fields=[
            "name",
            "age"
        ])

        employee_diagram = Diagram("Employee", fields=[
            "job_title"
        ], extends="Person")

        expected = ("class Person:\n"
                    "    def __init__(self, name, age):\n"
                    "        self.name = name\n"
                    "        self.age = age\n"
                    "\n"
                    "\n"
                    "class Employee(Person):\n"
                    "    def __init__(self, job_title):\n"
                    "        self.job_title = job_title\n"
                    "\n"
                    "\n"
                    )

        encoder = SourceCodeEncoder()
        person = encoder.generate_class(person_diagram)
        employee = encoder.generate_class(employee_diagram)
        actual = person + employee

        self.assertEqual(expected, actual)

    def test_generate_empty_class(self):
        airplane_diagram = Diagram("Airplane", fields=[
            "wing"
        ])

        wing_diagram = Diagram("Wing")

        expected = ("class Airplane:\n"
                    "    def __init__(self, wing):\n"
                    "        self.wing = wing\n"
                    "\n"
                    "\n"
                    "class Wing:\n"
                    "    pass\n"
                    "\n"
                    )

        encoder = SourceCodeEncoder()
        airplane = encoder.generate_class(airplane_diagram)
        wing = encoder.generate_class(wing_diagram)

        actual = airplane + wing
        self.assertEqual(expected, actual)

    def test_generate_class_with_dependence(self):
        style_diagram = Diagram("Style", methods=[
            {"signature": "get_cabinet()", "body": "return XCabinet()"}
        ])

        xcabinet_diagram = Diagram("XCabinet")

        expected = ("class Style:\n"
                    "    def get_cabinet(self):\n"
                    "        return XCabinet()\n"
                    "\n"
                    "class XCabinet:\n"
                    "    pass\n"
                    "\n"
                    )

        encoder = SourceCodeEncoder()
        style = encoder.generate_class(style_diagram)
        xcabinet = encoder.generate_class(xcabinet_diagram)

        actual = style + xcabinet

        self.assertEqual(expected, actual)

    def test_generate_class_with_method_params_as_object(self):
        style_diagram = Diagram("Style", methods=[
            {"signature": "get_cabinet(height)", "body": "return XCabinet()"}
        ])

        xcabinet_diagram = Diagram("XCabinet")

        expected = ("class Style:\n"
                    "    def get_cabinet(self, height):\n"
                    "        return XCabinet()\n"
                    "\n"
                    "class XCabinet:\n"
                    "    pass\n"
                    "\n"
                    )

        encoder = SourceCodeEncoder()
        style = encoder.generate_class(style_diagram)
        xcabinet = encoder.generate_class(xcabinet_diagram)

        actual = style + xcabinet

        self.assertEqual(expected, actual)

    def test_generate_class_with_method_params(self):
        diagram = Diagram("MyClass", methods=[
            "crazy_method2Name(param1, param2)"
        ])

        expected = ("class MyClass:\n"
                    "    def crazy_method2Name(self, param1, param2):\n"
                    "        pass\n"
                    "\n"
                    )

        encoder = SourceCodeEncoder()
        actual = encoder.generate_class(diagram)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
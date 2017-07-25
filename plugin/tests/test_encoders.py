import unittest
from prexel.plugin.encoders import PrettyPrintEncoder, SourceCodeEncoder
from prexel.plugin.diagram import Diagram


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
                    " _____________________ \n")

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
                    " _____________________ \n")

        encoder = PrettyPrintEncoder()
        actual = encoder.generate_class(diagram)

        self.assertEqual(expected, actual)

    def test_generate_class_with_inheritance(self):
        pass  # TODO implement


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
            {"name": "get_cabinet()", "body": "return XCabinet()"}
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

    def test_generate_class_with_method_params(self):
        style_diagram = Diagram("Style", methods=[
            {"name": "get_cabinet(height)", "body": "return XCabinet()"}
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

if __name__ == '__main__':
    unittest.main()

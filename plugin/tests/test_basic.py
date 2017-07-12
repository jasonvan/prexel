import unittest
from prexel.plugin.encoders import PrettyPrintEncoder, SourceCodeEncoder


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
                    " --------------------- \n")
        methods = [
            "arrange_kitchen()",
            "place_floor_cabinet()",
            "place_wall_cabinet()"
        ]

        encoder = PrettyPrintEncoder()
        actual = encoder.generate_class_body(21, methods, [])

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

        expected = (" _____________________ \n"
                    "|       Kitchen       |\n"
                    "|---------------------|\n"
                    "|arrange_kitchen()    |\n"
                    "|place_floor_cabinet()|\n"
                    "|place_wall_cabinet() |\n"
                    " --------------------- \n")

        encoder = PrettyPrintEncoder()
        actual = encoder.generate_class(diagram_element)

        self.assertEqual(expected, actual)

    def test_generate_class_with_inheritance(self):
        pass  # TODO implement


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
        actual = encoder.generate_class(diagram_element)

        self.assertEqual(expected, actual)

    def test_generate_class_with_inheritance(self):
        person_diagram_element = {
            "name":"Person",
            "type":"class",
            "fields": [
                "name",
                "age"
            ]
        }

        employee_diagram_element = {
            "name":"Employee",
            "type":"class",
            "fields": [
                "job_title"
            ],
            "extends": "Person"
        }

        expected = ("class Person:\n"
                    "    def __init__(self, name, age):\n"
                    "        self.name = name\n"
                    "        self.age = age\n"
                    "\n"
                    "class Employee(Person):\n"
                    "    def __init__(self, job_title):\n"
                    "        self.job_title = job_title\n"
                    "\n"
                    )

        encoder = SourceCodeEncoder()
        person = encoder.generate_class(person_diagram_element)
        employee = encoder.generate_class(employee_diagram_element)
        actual = person + employee

        self.assertEqual(expected, actual)

    def test_generate_empty_class(self):
        airplace_element = {
            "name": "Airplane",
            "type": "class",
            "fields": [
                "wing"
            ]
        }

        wing_element = {
            "name": "Wing",
            "type": "class"
        }

        expected = ("class Airplane:\n"
                    "    def __init__(self, wing):\n"
                    "        self.wing = wing\n"
                    "\n"
                    "class Wing:\n"
                    "    pass\n")

        encoder = SourceCodeEncoder()
        airplane = encoder.generate_class(airplace_element)
        wing = encoder.generate_class(wing_element)

        actual = airplane + wing
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()

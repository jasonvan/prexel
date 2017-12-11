import unittest

from prexel.parser.lexer import Lexer
from prexel.parser.interpreter import Interpreter, InterpreterException
from prexel.parser.token import Token


class TestInterpreter(unittest.TestCase):
    """
    Test cases to exercise the Interpreter class.
    """
    def test_init(self):
        """
        Test the __init__() method.
        """
        text = "|Airplane <>-wings--> Wing"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)

        self.assertEqual(interpreter.current_token.type, Token.START_MARKER)
        self.assertEqual(interpreter.current_token.value, "|")

    def test_process_token(self):
        """
        Test the process_token() method which processes one token at
        a time. Also includes a test to confirm an error message is given
        if an improper token is given.
        """
        text = "|Airplane <>-wings--> Wing"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        interpreter.process_token(Token.START_MARKER)

        # Assert the current token is a CLASS_NAME
        self.assertEqual(interpreter.current_token.type, Token.CLASS_NAME)

        # Test error message is raised when the incorrect token processed
        with self.assertRaises(InterpreterException) as context:
            interpreter.process_token(Token.FIELD)

        self.assertTrue('Invalid Syntax' in str(context.exception))

    def test_start_marker(self):
        """
        Test the start_marker() method, which processes a START_MARKER
        token.
        """
        text = "|Airplane <>-wings--> Wing"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        interpreter.start_marker()

        self.assertEqual(interpreter.current_token.value, "Airplane")
        self.assertEqual(interpreter.current_token.type, Token.CLASS_NAME)

    def test_class_name(self):
        """
        Test the class_name() method, which processes a CLASS_NAME token.
        """
        text = "|Airplane <>-wings--> Wing"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        interpreter.start_marker()
        name = interpreter.class_name()

        self.assertEqual(name, "Airplane")

    def test_class_body(self):
        """
        Test the class_body() method, which processes FIELD and METHOD tokens
        """
        text = "|Airplane size color take_off()"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        interpreter.start_marker()

        interpreter.class_name()
        fields, methods = interpreter.class_body()

        self.assertEqual(fields, ["size", "color"])
        self.assertEqual(methods, ["take_off()"])

    def test_inheritance(self):
        """
        Test the inheritance() method, which processes an inheritance
        relationship.
        """
        text = "|Room height width >> Kitchen"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)

        interpreter.start_marker()
        interpreter.class_name()
        interpreter.class_body()

        self.assertTrue(interpreter.inheritance())

    def test_inheritance_with_error(self):
        """
        Test the inheritance() method, with an improper syntax
        """
        text = "|Kitchen >>"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)

        interpreter.start_marker()
        interpreter.class_name()

        # Should raise a InterpreterException
        with self.assertRaises(InterpreterException) as context:
            interpreter.inheritance()

        self.assertEqual(context.exception.args[0], "Missing child class "
                                                    "after \">>\"")

    def test_aggregation(self):
        """
        Test the aggregation() method,
        """
        text = "|Kitchen <>-cupboard--> Cupboard"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        interpreter.start_marker()
        interpreter.class_name()
        aggregation = interpreter.aggregation()

        self.assertEqual(aggregation["name"], "Cupboard")
        self.assertEqual(aggregation["instance_name"], "cupboard")

    def test_aggregation_with_missing_aggregation_name(self):
        """
        Test the aggregation() method,
        """
        text = "|Kitchen <>---> Cupboard"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)

        interpreter.start_marker()
        interpreter.class_name()
        aggregation = interpreter.aggregation()

        self.assertEqual(aggregation["name"], "Cupboard")
        self.assertEqual(aggregation["instance_name"], "cupboard")

    def test_aggregation_multi_line(self):
        """
        Test the aggregation() method using multi-line syntax
        """
        text = """
|Kitchen <>-cupboard--> Cupboard
|size
|color"""
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        interpreter.start_marker()
        interpreter.class_name()
        aggregation = interpreter.aggregation(include_following_tokens=False)
        fields, methods = interpreter.class_body()

        self.assertEqual(aggregation["instance_name"], "cupboard")
        self.assertEqual(aggregation["name"], "Cupboard")
        self.assertEqual(fields, ["size", "color"])

    def test_aggregation_single_class_aggregation(self):
        """
        Test the aggregation() method using multi-line syntax
        """
        text = "|Class1 <>-> Class2 class_2_field class_2_method()"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        interpreter.start_marker()
        interpreter.class_name()
        interpreter.class_body()
        aggregation = interpreter.aggregation()

        self.assertEqual(aggregation["instance_name"], "class2")
        self.assertEqual(aggregation["name"], "Class2")
        self.assertEqual(aggregation["fields"], ["class_2_field"])
        self.assertEqual(aggregation["methods"], ["class_2_method()"])

    def test_class_delimiter(self):
        """
        Test the inheritance() method, which processes an inheritance
        relationship.
        """
        text = "|Room height width >> Kitchen, Bathroom"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)

        interpreter.start_marker()
        interpreter.class_name()
        interpreter.class_body()
        interpreter.inheritance()
        interpreter.class_name()

        self.assertTrue(interpreter.class_delimiter())

    def test_class_delimiter_with_error(self):
        """
        Test the inheritance() method, which processes an inheritance
        relationship.
        """
        text = "|Room height width >> Kitchen,"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)

        interpreter.start_marker()
        interpreter.class_name()
        interpreter.class_body()
        interpreter.inheritance()
        interpreter.class_name()

        # Should raise a InterpreterException
        with self.assertRaises(InterpreterException) as context:
            interpreter.class_delimiter()

        self.assertEqual(context.exception.args[0], "The is no following "
                                                    "class name.")

    def test_evaluate(self):
        text = "|Kitchen color square_feet show_kitchen() >> Room width " \
               "height <>--> Door turn_handle(), AnotherRoom field1 " \
               "field2 <>1--*> Cupboard"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)
        main_class = interpreter.evaluate()

        # Main Class
        self.assertEqual(main_class.name, "Kitchen")
        self.assertEqual(main_class.fields, ["color", "square_feet"])
        self.assertEqual(main_class.methods, ["show_kitchen()"])
        self.assertEqual(len(main_class.sub_classes), 2)

        # Room subclass and its aggregated class
        room = main_class.sub_classes[0]
        door = room.aggregated_classes[0]

        self.assertEqual(room.name, "Room")
        self.assertEqual(room.fields, ["width", "height"])
        self.assertEqual(door.name, "Door")
        self.assertEqual(door.methods, ["turn_handle()"])

        # AnotherRoom subclass and its aggregated class
        another_room = main_class.sub_classes[1]
        cupboard = another_room.aggregated_classes[0]

        self.assertEqual(another_room.name, "AnotherRoom")
        self.assertEqual(another_room.fields, ["field1", "field2"])
        self.assertEqual(cupboard.name, "Cupboard")

    def test_evaluate_extra(self):
        text = "|Room size >> Kitchen color show_kitchen()" \
               " <>1-cupboard--*> Cupboard"

        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        main_class = interpreter.evaluate()

        # Main class
        self.assertEqual(main_class.name, "Room")
        self.assertEqual(main_class.fields, ["size"])

        # Kitchen subclass and its aggregated class
        kitchen = main_class.sub_classes[0]
        cupboard = kitchen.aggregated_classes[0]

        self.assertEqual(kitchen.name, "Kitchen")
        self.assertEqual(kitchen.fields, ["color"])
        self.assertEqual(kitchen.methods, ["show_kitchen()"])
        self.assertEqual(cupboard.name, "Cupboard")
        self.assertEqual(cupboard.instance_name, "cupboard")
        self.assertEqual(cupboard.left_multiplicity, "1")
        self.assertEqual(cupboard.right_multiplicity, "*")

    def test_evaluate_error(self):
        text = "|Kitchen color square_feet show_kitchen() <>-cupboards-->"
        lexer = Lexer(text)

        interpreter = Interpreter(lexer)

        # Test error message
        with self.assertRaises(InterpreterException) as context:
            interpreter.evaluate()

        self.assertEqual(context.exception.args[0],
                         "There is no class name following the aggregation.")

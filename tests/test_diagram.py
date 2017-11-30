import unittest

from prexel.models.diagram import (Diagram, AggregationDiagram,
                                   AggregationMultiplicity)


class TestDiagram(unittest.TestCase):
    def setUp(self):
        self.kitchen = Diagram(name="Kitchen")

    def tearDown(self):
        self.kitchen = None

    def test_init(self):
        self.assertEqual(self.kitchen.name, "Kitchen")
        self.assertEqual(len(self.kitchen.fields), 0)
        self.assertEqual(len(self.kitchen.methods), 0)
        self.assertEqual(len(self.kitchen.aggregated_classes), 0)
        self.assertEqual(len(self.kitchen.sub_classes), 0)

    def test_add_sub_class(self):
        fancy_kitchen = Diagram("FancyKitchen")
        self.kitchen.add_sub_class(fancy_kitchen)
        self.assertIn(fancy_kitchen, self.kitchen.sub_classes)

    def test_add_aggregated_class(self):
        cupboard = Diagram("Cupboard")
        self.kitchen.add_aggregated_class(cupboard)
        self.assertIn(cupboard, self.kitchen.aggregated_classes)

    def test_fields(self):
        self.kitchen.add_field("field_1")
        self.assertIn("field_1", self.kitchen.fields)

    def test_methods(self):
        self.kitchen.add_method("method_1()")
        self.assertIn("method_1()", self.kitchen.methods)


class TestAggregationDiagram(unittest.TestCase):
    def setUp(self):
        self.left_multi = AggregationMultiplicity("*", "1")
        self.right_multi = AggregationMultiplicity("1", "*")

        self.cupboard = AggregationDiagram("Cupboard",
                                           self.left_multi,
                                           self.right_multi)

    def test_init(self):
        self.assertEqual(self.cupboard.name, "Cupboard")
        self.assertEqual(self.cupboard.left_multiplicity, self.left_multi)
        self.assertEqual(self.cupboard.right_multiplicity, self.right_multi)

        self.assertEqual(self.cupboard.left_multiplicity.lower_value, "*")
        self.assertEqual(self.cupboard.left_multiplicity.upper_value, "1")

        self.assertEqual(self.cupboard.right_multiplicity.lower_value, "1")
        self.assertEqual(self.cupboard.right_multiplicity.upper_value, "*")

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

    def test__eg__(self):
        self.assertTrue(self.kitchen == Diagram(name="Kitchen"))
        self.assertFalse(self.kitchen == Diagram(name="kitchen"))

    def test_merge_fields(self):
        to_merge = Diagram(name="Kitchen", fields=["field1", "field2"])
        self.kitchen.merge(to_merge)
        self.assertEqual(self.kitchen.fields, ["field1", "field2"])

    def test_merge_methods(self):
        to_merge = Diagram(name="Kitchen",
                           methods=["method_1()", "method_2()"])
        self.kitchen.merge(to_merge)
        self.assertEqual(self.kitchen.methods, ["method_1()", "method_2()"])

    def test_merge_subclasses(self):
        parent_class_1 = Diagram(name="Kitchen",
                                 fields=[
                                     "field_1",
                                     "field_2",
                                 ])

        parent_class_2 = Diagram(name="Kitchen",
                                 fields=[
                                     "field_3",
                                     "field_4",
                                 ])

        sub_class_1 = Diagram(name="FancyKitchen",
                              fields=[
                                  "field_5",
                                   "field_6",
                              ])

        sub_sub_class_1 = Diagram(name="SuperFancyKitchen",
                                  fields=[
                                      "field_9",
                                      "field_10",
                                  ])

        sub_class_2 = Diagram(name="FancyKitchen",
                              fields=[
                                  "field_7",
                                  "field_8",
                              ])

        unique_sub_class_2 = Diagram(name="ModernKitchen",
                                     fields=[
                                         "unique_field_1",
                                         "unique_field_2",
                                     ])

        sub_sub_class_2 = Diagram(name="SuperFancyKitchen",
                                  fields=[
                                      "field_11",
                                      "field_12",
                                  ])

        sub_class_1.add_sub_class(sub_sub_class_1)
        sub_class_2.add_sub_class(sub_sub_class_2)
        parent_class_1.add_sub_class(sub_class_1)
        parent_class_2.add_sub_class(sub_class_2)
        parent_class_2.add_sub_class(unique_sub_class_2)
        parent_class_1.merge(parent_class_2)

        self.assertEqual(parent_class_1.fields,
                         ["field_1",
                          "field_2",
                          "field_3",
                          "field_4",
                          ])

        self.assertEqual(parent_class_1.sub_classes[0].fields,
                         ["field_5",
                          "field_6",
                          "field_7",
                          "field_8",
                          ])

        self.assertEqual(parent_class_1.sub_classes[1].fields,
                         ["unique_field_1",
                          "unique_field_2",
                          ])

        self.assertEqual(parent_class_1.sub_classes[0].sub_classes[0].fields,
                         ["field_9",
                          "field_10",
                          "field_11",
                          "field_12",
                          ])

    def test_merge_aggregated_classes(self):
        class_1 = Diagram(name="Kitchen", fields=["field_1", "field_2", ])
        class_2 = Diagram(name="Kitchen", fields=["field_3", "field_4", ])

        aggregated_class_1 = Diagram(name="Cupboard",
                                     fields=["field_5", "field_6", ])

        aggregated_class_2 = Diagram(name="Cupboard",
                                     fields=["field_7", "field_8", ])

        aggregated_class_3 = Diagram(name="Door",
                                     fields=["field_9", "field_10", ])

        class_1.add_aggregated_class(aggregated_class_1)
        class_2.add_aggregated_class(aggregated_class_2)
        class_2.add_aggregated_class(aggregated_class_3)
        class_1.merge(class_2)

        self.assertEqual(class_1.fields,
                         ["field_1",
                          "field_2",
                          "field_3",
                          "field_4",
                          ])

        self.assertEqual(class_1.aggregated_classes[0].name, "Cupboard")
        self.assertEqual(class_1.aggregated_classes[0].fields,
                         ["field_5",
                          "field_6",
                          "field_7",
                          "field_8", ])

        self.assertEqual(class_1.aggregated_classes[1].name, "Door")
        self.assertEqual(class_1.aggregated_classes[1].fields,
                         ["field_9",
                          "field_10", ])


class TestAggregationDiagram(unittest.TestCase):
    def setUp(self):
        self.left_multi = AggregationMultiplicity("*", "1")
        self.right_multi = AggregationMultiplicity("1", "*")

        self.cupboard = AggregationDiagram("Cupboard",
                                           self.left_multi,
                                           self.right_multi)

    def test_init(self):
        # TODO FIXME
        self.assertEqual(self.cupboard.name, "Cupboard")
        self.assertEqual(self.cupboard.left_multiplicity, self.left_multi)
        self.assertEqual(self.cupboard.right_multiplicity, self.right_multi)

        self.assertEqual(self.cupboard.left_multiplicity.lower_value, "*")
        self.assertEqual(self.cupboard.left_multiplicity.upper_value, "1")

        self.assertEqual(self.cupboard.right_multiplicity.lower_value, "1")
        self.assertEqual(self.cupboard.right_multiplicity.upper_value, "*")

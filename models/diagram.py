"""
TODO
3 Change name of class
4 make all params optional
"""
class Diagram:
    def __init__(self, name, fields=[], methods=[]):
        self.name = name
        self.fields = fields
        self.methods = methods
        self.sub_classes = []
        self.aggregated_classes = []

    def add_sub_class(self, sub_class):
        self.sub_classes.append(sub_class)

    def add_aggregated_class(self, aggregated_class):
        self.aggregated_classes.append(aggregated_class)

    def add_field(self, field):
        self.fields.append(field)

    def add_fields(self, fields):
        self.fields.extend(fields)

    def add_method(self, method):
        self.methods.append(method)

    def add_methods(self, methods):
        self.methods.extend(methods)


class AggregationDiagram(Diagram):
    def __init__(self, name, instance_name=None,
                 left_multiplicity=None, right_multiplicity=None,
                 fields=[], methods=[]):
        super().__init__(name, fields, methods)
        self.left_multiplicity = left_multiplicity
        self.instance_name = instance_name
        self.right_multiplicity = right_multiplicity


class AggregationMultiplicity():
    def __init__(self, lower_value, upper_value):
        self.lower_value = lower_value
        self.upper_value = upper_value


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

    def merge(self, other):
        if self != other:
            return

        # Add fields
        self.fields.extend(other.fields)

        # Add methods
        self.methods.extend(other.methods)

        # Subclasses TODO could be cleaned up
        if other.sub_classes:
            to_append = []

            for other_sub_class in other.sub_classes:
                for sub_class in self.sub_classes:
                    if other_sub_class == sub_class:
                        sub_class.merge(other_sub_class)
                    else:
                        if other_sub_class not in to_append:
                            to_append.append(other_sub_class)

            self.sub_classes.extend(to_append)

        # Aggregated classes TODO could be cleaned up
        if other.aggregated_classes:
            to_append = []

            for other_aggregated_class in other.aggregated_classes:
                for aggregated_class in self.aggregated_classes:
                    if other_aggregated_class == aggregated_class:
                        # TODO need to deal with multiplicity, instance_name
                        # etc
                        aggregated_class.merge(other_aggregated_class)
                    else:
                        if other_aggregated_class not in to_append:
                            to_append.append(other_aggregated_class)

            self.aggregated_classes.extend(to_append)

    def __eq__(self, other):
        return self.name == other.name


class AggregationDiagram(Diagram):
    def __init__(self, name=None, instance_name=None,
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


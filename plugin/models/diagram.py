from abc import ABCMeta


class Diagram(metaclass=ABCMeta):
    """
    Represents a diagram element for use with interpreter and encoder
     ____________
    |  Diagram   |
    |------------|
    |name        |
    |type        |
    |____________|
    """
    def __init__(self, name, type):
        self.name = name
        self.type = type
    # def __init__(self, name="", diagram_type="class",
    #              fields=None, methods=None, extends=None):
    #     self.name = name
    #     self.diagram_type = diagram_type
    #     self.fields = fields
    #     self.methods = methods
    #     self.extends = extends


class ClassDiagram(Diagram):
    def __init__(self, name="", fields=None, methods=None, extends=None):
        super().__init__(name, "class")
        self.fields = fields
        self.methods = methods
        self.extends = extends


class AggregationDiagram(Diagram):
    def __init__(self, name="", left_multiplicity=None, right_multiplicity=None):
        super().__init__(name, "aggregation")
        self.left_multiplicity = left_multiplicity
        self.right_multiplicity = right_multiplicity


class InheritanceDiagram(Diagram):
    def __init__(self, name=""):
        super().__init__(name, "inheritance")

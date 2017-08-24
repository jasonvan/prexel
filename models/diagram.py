from abc import ABCMeta


class Diagram:
    def __init__(self, main,
                 parent=None, inheritance=None,
                 aggregated=None, aggregation=None):
        self.main = main
        self.parent = parent
        self.inheritance = inheritance
        self.aggregated = aggregated
        self.aggregation = aggregation

    def merge(self, *diagrams):
        """
        TODO need to set this up so a diagram object can be merged together
        """
        pass


class DiagramPart(metaclass=ABCMeta):
    """
    Represents a abstract diagram element for use with interpreter and encoder
    """
    def __init__(self, name, type):
        self.name = name
        self.type = type


class ClassDiagramPart(DiagramPart):
    """
     ___________ 
    |DiagramPart|
    |___________|
    ∆
    |________________ 
    |ClassDiagramPart|
    |________________|

    """

    def __init__(self, name="", fields=None, methods=None, extends=None):
        super().__init__(name, "class")
        self.fields = fields
        self.methods = methods
        self.extends = extends


class AggregationDiagramPart(DiagramPart):
    """
     ___________ 
    |DiagramPart|
    |___________|
    ∆
    |______________________ 
    |AggregationDiagramPart|
    |______________________|

    """
    def __init__(self, name="", left_multiplicity=None, right_multiplicity=None):
        super().__init__(name, "aggregation")
        self.left_multiplicity = left_multiplicity
        self.right_multiplicity = right_multiplicity


class InheritanceDiagramPart(DiagramPart):
    """
     ___________ 
    |DiagramPart|
    |___________|
    ∆
    |______________________ 
    |InheritanceDiagramPart|
    |______________________|

    """
    def __init__(self, name=""):
        super().__init__(name, "inheritance")

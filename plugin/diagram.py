class Diagram:
    """

    """
    def __init__(self, name, diagram_type="class", fields=None,
                 methods=None, extends=None):
        self.name = name
        self.diagram_type = diagram_type
        self.fields = fields
        self.methods = methods
        self.extends = extends

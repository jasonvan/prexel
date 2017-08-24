from prexel.encoders.encoder import Encoder


class PrettyPrintEncoder(Encoder):
    """
    PrettyPrintEncoder is responsible for taking a diagram element
    and creating a pretty-printed version of the element.

    Output based on:
    https://github.com/jasonvan/prexel/blob/master/planning/entry-examples.md

     _______ 
    |Encoder|
    |_______|
    ∆
    |__________________ 
    |PrettyPrintEncoder|
    |------------------|
    |generate()        |
    |create_class()    |
    |__________________|

    """
    def generate(self, diagram):
        """
        This method returns a pretty-printed class diagram based on
        the provided diagram object.

        Precondition: Well-formed diagram element
        Returns: pretty-printed diagram
        TODO commend this method
        """
        result = ""
        main_class = ""

        if diagram.inheritance:
            main_class += PrettyPrintEncoder.create_class(diagram.main, True)
        else:
            main_class += PrettyPrintEncoder.create_class(diagram.main)

        if diagram.aggregation:
            aggregation_arrow = PrettyPrintEncoder.create_aggregation_arrow(diagram.aggregation)
            aggregated_class = PrettyPrintEncoder.create_class(diagram.aggregated)
            result += PrettyPrintEncoder.concat_aggregation(main_class,
                                              aggregation_arrow,
                                              aggregated_class)
        else:
            result += main_class

        if diagram.parent:
            parent = PrettyPrintEncoder.create_class(diagram.parent)
            if diagram.inheritance:
                parent += PrettyPrintEncoder.create_inheritance_arrow()

            result = parent + result

        return result

    @staticmethod
    def create_class(class_diagram, extends=False):
        # Need to measure the different elements of the class diagram to see
        # which is the longest string
        items_to_measure = list()
        items_to_measure.append(class_diagram.name)

        if class_diagram.methods:
            for method in class_diagram.methods:
                items_to_measure.append(method)

        if class_diagram.fields:
            for field in class_diagram.fields:
                items_to_measure.append(field)

        max_length = len(max(items_to_measure, key=len))

        """
        Create the class header
        """

        # Formatters
        header_top_formatter = " {:_^" + str(max_length) + "} \n"
        header_middle_formatter = "|{:^" + str(max_length) + "}|\n"
        header_bottom_formatter = "|{:-^" + str(max_length) + "}|\n"

        header_top = header_top_formatter.format("")
        header_middle = header_middle_formatter.format(class_diagram.name)
        header_bottom = header_bottom_formatter.format("")

        header = ""

        # Add extends bar "|" on far left side
        if extends:
            header_top = "|" + header_top[1:]

        header += header_top
        header += header_middle

        # Add cross bar underneath class name
        if class_diagram.fields or class_diagram.methods:
            header += header_bottom

        """
        Create the class body
        """

        # Formatters
        body_middle_formatter = "|{:<" + str(max_length) + "}|\n"
        body_bottom_formatter = "|{:_^" + str(max_length) + "}|\n"

        body = ""

        if class_diagram.fields:
            for field in class_diagram.fields:
                body += body_middle_formatter.format(field)

        if class_diagram.methods:
            for method in class_diagram.methods:
                body += body_middle_formatter.format(method)

        body += body_bottom_formatter.format("")

        # Result
        return header + body

    @staticmethod
    def create_aggregation_arrow(aggregation_diagram):
        result = "<>"
        if aggregation_diagram.left_multiplicity:
            result += aggregation_diagram.left_multiplicity

        result += "-{}---".format(aggregation_diagram.name)

        if aggregation_diagram.right_multiplicity:
            result += aggregation_diagram.right_multiplicity

        result += ">"

        return result

    @staticmethod
    def create_inheritance_arrow():
        """
        Will be expanded later
        """
        return "∆\n"

    @staticmethod
    def concat_aggregation(aggregator, aggregation, aggregated):
        result = []
        aggregator_parts = list(filter(None, aggregator.split("\n")))
        aggregated_parts = list(filter(None, aggregated.split("\n")))

        length_aggregator = len(max(aggregator_parts))
        length_aggregated = len(max(aggregated_parts))
        length_aggregation = len(aggregation)

        height_aggregator = len(aggregator_parts)
        height_aggregated = len(aggregated_parts)

        combined = zip(aggregator_parts, aggregated_parts)
        combined_list = list(combined)
        start_index = len(combined_list)

        for index, item in enumerate(combined_list):
            line = item[0]
            if index == 1:
                line += aggregation
            else:
                line += " " * length_aggregation

            line += item[1]

            result.append(line)

        if height_aggregator > height_aggregated:
            for item in aggregator_parts[start_index:]:
                line = item
                line += " " * length_aggregation
                line += " " * length_aggregated
                result.append(line)
        elif height_aggregated > height_aggregator:
            for item in aggregated_parts[start_index:]:
                line = " " * length_aggregator
                line += " " * length_aggregation
                line += item
                result.append(line)
        else:
            pass  # If they are the same length they are already combined

        return "\n".join(result) + "\n"

from prexel.plugin.encoders.encoder import Encoder


class PrettyPrintEncoder(Encoder):
    """
    PrettyPrintEncoder is responsible for taking a diagram element
    and creating a pretty-printed version of the element.

    Output based on:
    https://github.com/jasonvan/prexel/blob/master/planning/entry-examples.md

     ---------
    | Encoder |
    |_________|
       ^
     ----------------------
    |  PrettyPrintEncoder  |        ---------
    |----------------------|------>| Diagram |
    |generate_class()      |       |_________|
    |______________________|
    """
    def generate_class(self, diagram):
        """
        This method returns a pretty-printed class diagram based on
        the provided diagram object.

        Precondition: Well-formed diagram element
        Returns: pretty-printed diagram
        """

        # Need to measure the different elements of the diagram to see
        # which is the longest string
        items_to_measure = list()

        # Name
        items_to_measure.append(diagram.name)

        # Methods
        if diagram.methods:
            for method in diagram.methods:
                items_to_measure.append(method)

        # Fields
        if diagram.fields:
            for field in diagram.fields:
                items_to_measure.append(field)

        # Determine max length of longest string in class
        max_length = len(max(items_to_measure, key=len))

        # Create the class header and the body
        result = ""
        result += self.generate_class_header(max_length, diagram)
        result += self.generate_class_body(max_length, diagram)

        return result

    def generate_class_body(self, max_length, diagram):
        """
        Generate the class body string for the provided diagram.
        Returns: class body string
        """

        # Create formatters that will properly space the body string
        middle_formatter = "|{:<" + str(max_length) + "}|\n"
        bottom_formatter = "|{:_^" + str(max_length) + "}|\n"

        # Generate the body string
        body = ""

        if diagram.fields:
            for field in diagram.fields:
                body += middle_formatter.format(field)

        if diagram.methods:
            for method in diagram.methods:
                body += middle_formatter.format(method)

        body += bottom_formatter.format("")

        return body

    def generate_class_header(self, max_length, diagram):
        """
        Generate the class header from the provided diagram name.
        Returns: class header string
        """

        max_length_as_string = str(max_length)

        # Create formatters
        extends_formatter = "∆{:^" + max_length_as_string + "} \n"
        top_formatter = " {:_^" + max_length_as_string + "} \n"
        middle_formatter = "|{:^" + max_length_as_string + "}|\n"
        bottom_formatter = "|{:-^" + max_length_as_string + "}|\n"

        # Create strings
        top = top_formatter.format("")
        middle = middle_formatter.format(diagram.name)
        bottom = bottom_formatter.format("")

        # Assemble header
        header = ""

        # Add extends and arrow and update the top value with a "|"
        # on the far left side
        if diagram.extends:
            extends = extends_formatter.format("")
            header += extends

            top = "|" + top[1:]

        header += top
        header += middle
        if diagram.fields or diagram.methods:
            header += bottom

        return header

    def generate_aggregation(self, diagram):
        result = "<>"
        if diagram.left_multiplicity:
            result += diagram.left_multiplicity

        result += "-{}---".format(diagram.name)

        if diagram.right_multiplicity:
            result += diagram.right_multiplicity

        result += ">"

        return result

    def concat_inheritance(self, parent, children):
        results = parent
        for child_class in children:
            results += child_class

        return results

    def concat_aggregation(self, aggregator, aggregation, aggregated):
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

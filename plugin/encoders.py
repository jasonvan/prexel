class PrettyPrintEncoder:
    def generate_class(self, diagram_element):
        items_to_measure = []

        try:
            name = diagram_element["name"]
        except KeyError as error:
            pass  # TODO deal with this error
        else:
            items_to_measure += [name]

        try:
            methods = diagram_element["methods"]
        except KeyError as error:
            pass  # TODO deal with this error
        else:
            items_to_measure += methods

        try:
            fields = diagram_element["fields"]
        except KeyError as error:
            pass  # TODO deal with this error
        else:
            items_to_measure += fields

        # Determine max length of longest string in class
        max_length = len(max(items_to_measure, key=len))

        # Create the class header and the body
        class_header = self.generate_class_header(max_length, name)
        class_body = self.generate_class_body(max_length, methods)

        return class_header + class_body

    def generate_class_body(self, max_length, methods=[], fields=[]):
        middle_formatter = "|{:<" + str(max_length) + "}|\n"
        bottom_formatter = " {:-^" + str(max_length) + "} \n"

        middle = ""

        for field in fields:
            middle += middle_formatter.format(field)

        for method in methods:
            middle += middle_formatter.format(method)

        bottom = bottom_formatter.format("")

        return middle + bottom

    def generate_class_header(self, max_length, name):
        top_formatter = "\n {:_^" + str(max_length) + "} \n"
        middle_formatter = "|{:^" + str(max_length) + "}|\n"
        bottom_formatter = "|{:-^" + str(max_length) + "}|\n"

        top = top_formatter.format("")
        middle = middle_formatter.format(name)
        bottom = bottom_formatter.format("")

        return top + middle + bottom

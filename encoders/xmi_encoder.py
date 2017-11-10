import random
import string
from prexel.regex import REGEX
from xml.dom.minidom import Document
from prexel.encoders.encoder import Encoder


class XMIEncoder(Encoder):
    """
     _______ 
    |Encoder|
    |_______|
    ∆
    |__________ 
    |XMIEncoder|
    |----------|
    |generate()|
    |__________|

    """
    def generate(self, diagram, display_id=True):
        generator = XMIDocumentGenerator(display_id)
        document = generator.document

        # Diagram values
        main = diagram.main
        parent = diagram.parent
        aggregated = diagram.aggregated
        aggregation = diagram.aggregation

        # Create the base elements
        xmi_element = generator.xmi_element()
        documentation_node = generator.documentation_element("Prexel", "1.0")
        uml_element = generator.uml_element("RootModel")

        # Append them to the document
        xmi_element.appendChild(documentation_node)
        xmi_element.appendChild(uml_element)
        document.appendChild(xmi_element)

        # Add parent class to XMI if present
        if parent:
            parent_class = generator.class_element(parent.name)
            parent_id = self._get_id(parent_class)

            # Add fields and methods
            self._add_fields_and_methods(parent.fields,
                                         parent.methods,
                                         parent_class,
                                         generator)

            uml_element.appendChild(parent_class)

        # Add main class to XMI
        if main:
            main_class = generator.class_element(main.name)
            main_id = self._get_id(main_class)

            # Add fields and methods
            self._add_fields_and_methods(main.fields,
                                         main.methods,
                                         main_class,
                                         generator)

            # Create inheritance connection if parent class exists
            if parent:
                main_class.appendChild(generator.generalization(main_id,
                                                                parent_id))

            # Add the main_class the UML element
            uml_element.appendChild(main_class)

        if aggregated and aggregation:
            aggregated_class = generator.class_element(aggregated.name)
            aggregated_class_id = self._get_id(aggregated_class)

            # Add fields and methods for class
            self._add_fields_and_methods(aggregated.fields,
                                         aggregated.methods,
                                         aggregated_class,
                                         generator)

            # Create owned_member
            owned_member = generator.owned_member(aggregation.name)

            # Create owned ends
            owned_end_none = generator.owned_end(main_id)
            owned_end_shared = generator.owned_end(aggregated_class_id,
                                                   shared=True)
            # Add multiplicity to owned ends
            self._add_multiplicity_values(aggregation.left_multiplicity,
                                          owned_end_none,
                                          generator)

            self._add_multiplicity_values(aggregation.right_multiplicity,
                                          owned_end_shared,
                                          generator)

            # Generate member_ends
            owned_end_none_id = self._get_id(owned_end_none)
            owned_end_shared_id = self._get_id(owned_end_shared)
            member_end_first = generator.member_end(owned_end_none_id)
            member_end_second = generator.member_end(owned_end_shared_id)

            # Append all the generated elements
            owned_member.appendChild(owned_end_none)
            owned_member.appendChild(owned_end_shared)
            owned_member.appendChild(member_end_first)
            owned_member.appendChild(member_end_second)
            aggregated_class.appendChild(owned_member)
            uml_element.appendChild(aggregated_class)

        # Convert DOM model to string
        xmi = document.toprettyxml(encoding="UTF-8").decode()

        # Need to replace all instances of "xmi-type".
        # See XMIDocumentGenearator#owned_end for more info
        xmi = xmi.replace("xmi-type", "xmi:type")

        return xmi

    def _add_fields_and_methods(self, fields, methods, class_element, generator):
        if fields:
            for field in fields:
                owned_attribute = generator.owned_attribute(field)
                class_element.appendChild(owned_attribute)

        if methods:
            for method in methods:
                # Remove the method signature
                m = REGEX["method_signature"].match(method)
                if m.group(1):
                    method = m.group(1)

                owned_operation = generator.owned_operation(method)
                class_element.appendChild(owned_operation)

    def _add_multiplicity_values(self, multiplicity, owned_end, generator):
        if multiplicity:
            if REGEX["valid_multiplicity"].match(multiplicity):
                if multiplicity == "*":
                    lower_value = generator.lower_value(
                        "uml:LiteralUnlimitedNatural",
                        multiplicity
                    )
                    upper_value = generator.upper_value(
                        "uml:LiteralUnlimitedNatural",
                        multiplicity
                    )
                else:
                    lower_value = generator.lower_value(
                        "uml:LiteralInteger",
                        multiplicity
                    )
                    upper_value = generator.upper_value(
                        "uml:LiteralInteger",
                        multiplicity
                    )

                owned_end.appendChild(lower_value)
                owned_end.appendChild(upper_value)

    def _get_id(self, element):
        return element.getAttribute("xmi:id")


class XMIDocumentGenerator:

    """
    This class facilitates the conversion to XMI from a Diagram object. A 
    Diagram object is main model used to transfer UML data from the parsers to
    the encoders.
     ___________ 
    |  Diagram  |
    |-----------|
    |main       |
    |parent     |
    |inheritance|
    |aggregated |
    |aggregation|
    |___________|

    As there are several different schemas for XMI, we want it to fairly 
    straight-forward to switch between them without having to update the 
    parsers or encoder code

    """

    def __init__(self, display_id):
        self.display_id = display_id
        self.document = Document()

    def xmi_element(self):
        element = self.document.createElement("xmi:XMI")
        element.setAttribute("xmi:version", "2.1")
        element.setAttribute("xmlns:uml", "http://schema.omg.org/spec/UML/2.0")
        element.setAttribute("xmlns:xmi", "http://schema.omg.org/spec/XMI/2.1")

        return element

    def documentation_element(self, name, version):
        element = self.document.createElement("xmi:Documentation")
        element.setAttribute("exporter", name)
        element.setAttribute("exporterVersion", version)

        return element

    def uml_element(self, name):
        element = self.document.createElement("uml:Model")
        element.setAttribute("name", name)
        element.setAttribute("xmi:type", "uml:Model")
        element.setAttribute("xmi:id", self.generate_id())

        return element

    def model_element(self, name, **kwargs):
        return self.package_element("uml:Model", name, **kwargs)

    def class_element(self, name, **kwargs):
        return self.package_element("uml:Class", name, **kwargs)

    def package_element(self, xmi_type, name, **kwargs):
        valid_attributes = (
            "visibility",
            "isAbstract",
            "isFinalSpecialization",
            "isLeaf",
            "isActive",
        )

        package_element = self.document.createElement("packagedElement")
        package_element.setAttribute("xmi:type", xmi_type)
        package_element.setAttribute("name", name)
        self._add_id(package_element)

        # Set default attributes if not provided
        if not kwargs:
            kwargs = {
                "visibility": "public",
                "isAbstract": "false",
                "isFinalSpecialization": "false",
                "isLeaf": "false",
                "isActive": "false"
            }

        self._add_attributes(package_element, valid_attributes, **kwargs)
        return package_element

    def owned_attribute(self, name, **kwargs):
        valid_attributes = (
            "visibility",
            "isStatic",
            "isLeaf",
            "isReadOnly",
            "isOrdered",
            "isUnique",
            "aggregation",
            "isDerived",
            "isID",
        )

        owned_attribute = self.document.createElement("ownedAttribute")
        owned_attribute.setAttribute("xmi:type", "uml:Property")
        owned_attribute.setAttribute("name", name)
        self._add_id(owned_attribute)

        # Set default attributes if not provided
        if not kwargs:
            kwargs = {
                "visibility": "public",
                "isStatic": "false",
                "isLeaf": "false",
                "isReadOnly": "false",
                "isOrdered": "false",
                "isUnique": "false",
                "aggregation": "none",
                "isDerived": "false",
                "isID": "false"
            }

        self._add_attributes(owned_attribute, valid_attributes, **kwargs)
        return owned_attribute

    def owned_operation(self, name, **kwargs):
        valid_attributes = (
            "visibility",
            "isAbstract",
            "isFinalSpecialization",
            "isLeaf",
            "isActive",
            "concurrency",
            "isStatic",
            "isQuery",
        )

        owned_operation = self.document.createElement("ownedOperation")
        owned_operation.setAttribute("xmi:type", "uml:Operation")
        owned_operation.setAttribute("name", name)
        self._add_id(owned_operation)

        # Set default attributes if not provided
        if not kwargs:
            kwargs = {
                "visibility": "public",
                "isStatic": "false",
                "isLeaf": "false",
                "concurrency": "sequential",
                "isQuery": "false",
                "isAbstract": "false"
            }

        self._add_attributes(owned_operation, valid_attributes, **kwargs)
        return owned_operation

    def owned_member(self, name, **kwargs):
        valid_attributes = (
            "name",
            "visibility",
            "isDerived",
        )

        owned_member = self.document.createElement("ownedMember")
        owned_member.setAttribute("xmi:type", "uml:Association")
        owned_member.setAttribute("name", name)
        self._add_id(owned_member)

        # Set default attributes if not provided
        if not kwargs:
            kwargs = {
                "visibility": "public",
                "isDerived": "false"
            }

        self._add_attributes(owned_member, valid_attributes, **kwargs)
        return owned_member

    def owned_end(self, type, shared=False, **kwargs):
        valid_attributes = (
            "type",
            "visibility",
            "isStatic",
            "isLeaf",
            "isReadOnly",
            "isOrdered",
            "isUnique",
            "aggregation",
            "isDerived",
            "isID",
        )

        owned_end = self.document.createElement("ownedEnd")

        # The attribute "xmi-type" below isn't actually correct, but
        # the DOM library used (MiniDOM) overwrites any attribute name that
        # already exists even if it proceeded by a XML namespace.
        # Example: "xmi:type" attribute is replaced with the "type" attribute
        # value. Using "xmi-type" allows for this to be replaced with
        # "xmi:type" after the XML is converted to a string.
        owned_end.setAttribute("xmi-type", "uml:Property")
        owned_end.setAttribute("type", type)
        self._add_id(owned_end)

        # Set default attributes if not provided
        if not kwargs:
            kwargs = {
                "visibility": "public",
                "isStatic": "false",
                "isLeaf": "false",
                "isReadOnly": "false",
                "isOrdered": "false",
                "isUnique": "false",
                "aggregation": "none",
                "isDerived": "false",
                "isID": "false",
            }

            if shared:
                kwargs["aggregation"] = "shared"

        self._add_attributes(owned_end, valid_attributes, **kwargs)
        return owned_end

    def member_end(self, idref):
        member_end = self.document.createElement("memberEnd")
        member_end.setAttribute("xmi:idref", idref)
        return member_end

    def upper_value(self, type, value):
        upper_value = self.document.createElement("upperValue")
        upper_value.setAttribute("xmi:type", type)
        upper_value.setAttribute("value", value)
        self._add_id(upper_value)

        return upper_value

    def lower_value(self, type, value):
        lower_value = self.document.createElement("lowerValue")
        lower_value.setAttribute("xmi:type", type)
        lower_value.setAttribute("value", value)
        self._add_id(lower_value)

        return lower_value

    def generalization(self, specific, general, **kwargs):
        valid_attributes = (
            "visibility",
            "specific",
            "general",
        )

        generalization = self.document.createElement("generalization")
        generalization.setAttribute("specific", specific)
        generalization.setAttribute("general", general)
        generalization.setAttribute("xmi:type", "uml:Generalization")

        self._add_attributes(generalization, valid_attributes, **kwargs)

        return generalization

    def _add_id(self, elem):
        generated_id = self.generate_id()
        elem.setAttribute("xmi:id", generated_id)
        return generated_id

    def _add_attributes(self, elem, valid_attributes, **kwargs):
        for key, value in kwargs.items():
            if key in valid_attributes:
                elem.setAttribute(key, value)

    def generate_id(self):
        char_set = string.ascii_letters + string.digits
        if self.display_id:
            generate_id = "AAAAAAF" + ''.join([random.choice(char_set) for n in range(10)])
        else:
            generate_id = ""
        return generate_id

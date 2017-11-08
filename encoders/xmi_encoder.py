import random
import string
from collections import OrderedDict
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

        main_id = None
        parent_id = None

        # Add in the Diagram specific elements
        if parent:
            parent_class = generator.class_element(
                name=parent.name,
                visibility="public"
            )

            parent_id = self._get_id(parent_class)

            if parent.fields:
                for field in parent.fields:
                    parent_class.appendChild(generator.owned_attribute(
                        name=field))

            uml_element.appendChild(parent_class)

        if main:
            # Create the main class element
            main_class = generator.class_element(
                name=main.name,
                visibility="public",
                isAbstract="false",
                isFinalSpecialization="false",
                isLeaf="false",
                isActive="false"
            )

            main_id = self._get_id(main_class)

            # Append the methods
            if main.methods:
                for method in main.methods:
                    # Remove the method signature
                    m = REGEX["method_signature"].match(method)
                    if m.group(1):
                        method = m.group(1)

                    main_class.appendChild(generator.owned_operation(
                        name=method))

            # Append the fields
            if main.fields:
                for field in main.fields:
                    main_class.appendChild(generator.owned_attribute(
                        name=field))

            if parent and parent_id:
                main_class.appendChild(generator.generalization(main_id,
                                                                parent_id))

            # Add the main_class the UML element
            uml_element.appendChild(main_class)

        if aggregated and aggregation:
            aggregated_class = generator.class_element(
                name=aggregated.name,
                visibility="public",
                isAbstract="false",
                isFinalSpecialization="false",
                isLeaf="false",
                isActive="false"
            )

            aggregated_class_id = self._get_id(aggregated_class)

            owned_member = generator.owned_member(
                name=aggregation.name,
                visibility="public",
                isDerived="false"
            )

            owned_end_none = generator.owned_end(
                visibility="public",
                isStatic="false",
                isLeaf="false",
                isReadOnly="false",
                isOrdered="false",
                isUnique="false",
                aggregation="none",
                isDerived="false",
                isID="false",
                type=main_id
            )

            owned_end_shared = generator.owned_end(
                visibility="public",
                isStatic="false",
                isLeaf="false",
                isReadOnly="false",
                isOrdered="false",
                isUnique="false",
                aggregation="shared",
                isDerived="false",
                isID="false",
                type=aggregated_class_id
            )

            member_end_first = generator.member_end(
                self._get_id(owned_end_none))
            member_end_second = generator.member_end(
                self._get_id(owned_end_shared))

            owned_member.appendChild(owned_end_none)
            owned_member.appendChild(owned_end_shared)
            owned_member.appendChild(member_end_first)
            owned_member.appendChild(member_end_second)

            aggregated_class.appendChild(owned_member)
            uml_element.appendChild(aggregated_class)

        return document.toprettyxml(encoding="UTF-8").decode()

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

    def model_element(self, **kwargs):
        return self.package_element("uml:Model", **kwargs)

    def class_element(self, **kwargs):
        return self.package_element("uml:Class", **kwargs)

    def package_element(self, xmi_type, **kwargs):
        valid_attributes = (
            "name",
            "visibility", 
            "isAbstract",
            "isFinalSpecialization",
            "isLeaf",
            "isActive",
        )

        package_element = self.document.createElement("packagedElement")
        package_element.setAttribute("xmi:type", xmi_type)

        self._add_id(package_element)
        self._add_attributes(package_element, valid_attributes, **kwargs)

        return package_element

    def owned_attribute(self, **kwargs):
        valid_attributes = (
            "name",
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

        self._add_attributes(owned_attribute, valid_attributes, **kwargs)
        self._add_id(owned_attribute)

        return owned_attribute

    def owned_operation(self, **kwargs):
        valid_attributes = (
            "name",
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

        self._add_id(owned_operation)
        self._add_attributes(owned_operation, valid_attributes, **kwargs)

        return owned_operation

    def owned_member(self, **kwargs):
        valid_attributes = (
            "name",
            "visibility",
            "isDerived",
        )

        owned_member = self.document.createElement("ownedMember")
        owned_member.setAttribute("xmi:type", "uml:Association")

        self._add_attributes(owned_member, valid_attributes, **kwargs)
        self._add_id(owned_member)

        return owned_member

    def owned_end(self, **kwargs):
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
        # already exists even if it proceeded by an XML namespace.
        # Example: xmi:type is replace with the type attribute value
        # Using "xmi-type" allows for this to be replace with "xmi:type" after
        # the XML is converted to a string
        owned_end.setAttribute("xmi-type", "uml:Association")

        self._add_attributes(owned_end, valid_attributes, **kwargs)
        self._add_id(owned_end)

        return owned_end

    def member_end(self, idref):
        member_end = self.document.createElement("memberEnd")
        member_end.setAttribute("xmi:idref", idref)
        return member_end

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

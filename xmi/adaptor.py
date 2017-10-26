import random
import string
from xml.dom.minidom import Document


class XMIAdaptor:

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

    TODO: make name and type part of **kwargs
    """

    def __init__(self):
        self.document = Document()

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

        return self._add_attributes(package_element,
                                    valid_attributes, 
                                    **kwargs)

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

        return self._add_attributes(owned_attribute,
                                    valid_attributes,
                                    **kwargs)

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

        return self._add_attributes(owned_operation, 
                                    valid_attributes,
                                    **kwargs)

    def owned_member(self, **kwargs):
        valid_attributes = (
            "name",
            "visibility",
            "isDerived",
        )

        owned_member = self.document.createElement("ownedMember")
        owned_member.setAttribute("xmi:type", "uml:Association")

        return self._add_attributes(owned_member,
                                    valid_attributes,
                                    **kwargs)

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
        owned_end.setAttribute("xmi:type", "uml:Association")

        return self._add_attributes(owned_end,
                                    valid_attributes,
                                    **kwargs)

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

        return self._add_attributes(generalization,
                                    valid_attributes,
                                    **kwargs)

    def _add_attributes(self, elem, valid_attributes, **kwargs):
        id = self._generate_id()

        elem.setAttribute("xmi:id", id)

        for key, value in kwargs.items():
            if key in valid_attributes:
                elem.setAttribute(key, value)

        return (id, elem)

    def _generate_id(self):
        """
        TODO
        """
        char_set = string.ascii_letters + string.digits
        id = "AAAAAAF" + ''.join([random.choice(char_set) for n in range(10)])
        return id

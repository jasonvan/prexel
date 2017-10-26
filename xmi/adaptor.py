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
    """

    def __init__(self):
        self.document = Document()

    def model_element(self, name, **kwargs):
        """
        TODO
        """
        return self.package_element("uml:Model", name, **kwargs)

    def class_element(self, name, **kwargs):
        """
        TODO
        """
        return self.package_element("uml:Class", name, **kwargs)

    def package_element(self, type, name="", **kwargs):
        """
        TODO
        """
        valid_attributes = (
            "visibility", 
            "isAbstract",
            "isFinalSpecialization",
            "isLeaf",
            "isActive",
        )

        package_element = self.document.createElement("packagedElement")
        return self._add_attributes(package_element,
                                    type,
                                    valid_attributes, 
                                    name,
                                    **kwargs)

    def owned_attribute(self, name, **kwargs):
        """
        TODO
        """
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
        return self._add_attributes(owned_attribute,
                                    "uml:Property",
                                    valid_attributes, 
                                    name,
                                    **kwargs)

    def owned_operation(self, name, **kwargs):
        """
        TODO
        """
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
        return self._add_attributes(owned_operation, 
                                    "uml:Operation",
                                    valid_attributes, 
                                    name,
                                    **kwargs)

    def owned_member(self, name, **kwargs):
        valid_attributes = (
            "visibility",
            "isDerived",
        )

        owned_member = self.document.createElement("ownedMember")
        return self._add_attributes(owned_member,
                                    "uml:Association",
                                    valid_attributes,
                                    name,
                                    **kwargs)

    def owned_end(self, name, **kwargs):
        pass  # TODO

    def member_end(self, **kwargs):
        pass  # TODO

    def member_end(self, **kwargs):
        pass  # TODO

    def generalization(self, specific, general, **kwargs):
        valid_attributes = (
            "visibility",
            "specific",
            "general",
        )

        generalization = self.document.createElement("generalization")
        generalization.setAttribute("specific", specific)
        generalization.setAttribute("general", general)

        return self._add_attributes(generalization,
                                    "uml:Generalization",
                                    valid_attributes,
                                    **kwargs)

    def _add_attributes(self, elem, type, valid_attributes, name="", **kwargs):
        """
        TODO
        """
        id = self._generate_id()

        elem.setAttribute("xmi:id", id)
        if name:
            elem.setAttribute("name", name)
        elem.setAttribute("xmi:type", type)

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

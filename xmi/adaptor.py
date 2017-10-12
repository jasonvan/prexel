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
        return self.package_element(name, "uml:Model", **kwargs)

    def class_element(self, name, **kwargs):
        """
        TODO
        """
        return self.package_element(name, "uml:Class", **kwargs)

    def package_element(self, name, type, **kwargs):
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
                                    name,
                                    type,
                                    valid_attributes, 
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
                                    name,
                                    "uml:Property",
                                    valid_attributes, 
                                    **kwargs)

    def owned_operation(self, name, **kwargs):
        """
        TODO
        """
        valid_attributes = (
            "visibility"
            "isAbstract"
            "isFinalSpecialization"
            "isLeaf"
            "isActive"
            "concurrency"
            "isStatic"
            "isQuery"
        )

        owned_operation = self.document.createElement("ownedOperation")
        return self._add_attributes(owned_operation, 
                                    name,
                                    "uml:Operation",
                                    valid_attributes, 
                                    **kwargs)

    def owned_member(self, name, **kwargs):
        pass  # TODO

    def owned_end(self, name, **kwargs):
        pass  # TODO

    def member_end(self, **kwargs):
        pass  # TODO

    def member_end(self, **kwargs):
        pass  # TODO

    def generalization(self, **kwargs):
        pass  # TODO

    def _add_attributes(self, elem, name, type, valid_attributes, **kwargs):
        """
        TODO
        """
        id = self._generate_id()

        elem.setAttribute("xmi:id", id)
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

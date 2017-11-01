import unittest
from xml.dom.minidom import Document
from prexel.xmi.adaptor import XMIAdaptor


class TestXMIAdaptor(unittest.TestCase):
    """
    Main methods of XMIAdaptor class
     _________________ 
    |   XMIAdaptor    |
    |-----------------|
    |package_element()|
    |model_element()  |
    |class_element()  |
    |owned_attribute()|
    |owned_operation()|
    |_________________|

    """
    def setUp(self):
        self.xmi_adapator = XMIAdaptor()

    def test_add_attributes(self):
        package_element = Document().createElement("packagedElement")
        valid_attributes = (
            "name",
            "attr1",
            "attr2",
            "attr3",
            "attr4",
            "attr5",
        )

        self.xmi_adapator._add_attributes(
            package_element, 
            valid_attributes,
            name="Model",
            attr1="attr1",
            attr2="attr2",
            attr3="attr3",
            attr6="attr6"
        )

        self.assertEqual(package_element.getAttribute("name"), "Model")
        self.assertEqual(package_element.getAttribute("attr1"), "attr1")
        self.assertEqual(package_element.getAttribute("attr2"), "attr2")
        self.assertEqual(package_element.getAttribute("attr6"), "")

    def test_package_element(self):
        elem = self.xmi_adapator.package_element(
            "uml:Model", 
            name="Model", 
            visibility="public")

        self.assertEqual(elem.getAttribute("name"), "Model")
        self.assertEqual(elem.getAttribute("xmi:type"), "uml:Model")
        self.assertEqual(elem.getAttribute("visibility"), "public")

        elem = self.xmi_adapator.package_element(
            "uml:Class", 
            name="Kitchen", 
            visibility="public",
            isAbstract="false",
            isFinalSpecialization="false",
            isLeaf="false",
            isActive="false")

        self.assertEqual(elem.getAttribute("name"), "Kitchen")
        self.assertEqual(elem.getAttribute("xmi:type"), "uml:Class")
        self.assertEqual(elem.getAttribute("visibility"), "public")
        self.assertEqual(elem.getAttribute("isAbstract"), "false")
        self.assertEqual(elem.getAttribute("isFinalSpecialization"), "false")
        self.assertEqual(elem.getAttribute("isLeaf"), "false")
        self.assertEqual(elem.getAttribute("isActive"), "false")

    def test_model_element(self):
        elem = self.xmi_adapator.model_element(
            name="Model",
            visibility="public")

        self.assertEqual(elem.getAttribute("name"), "Model")
        self.assertEqual(elem.getAttribute("xmi:type"), "uml:Model")
        self.assertEqual(elem.getAttribute("visibility"), "public")

    def test_class_element(self):
        elem = self.xmi_adapator.class_element(
            name="Kitchen",
            visibility="public",
            isAbstract="false",
            isFinalSpecialization="false",
            isLeaf="false",
            isActive="false")

        self.assertEqual(elem.getAttribute("name"), "Kitchen")
        self.assertEqual(elem.getAttribute("xmi:type"), "uml:Class")
        self.assertEqual(elem.getAttribute("visibility"), "public")
        self.assertEqual(elem.getAttribute("isAbstract"), "false")
        self.assertEqual(elem.getAttribute("isFinalSpecialization"), "false")
        self.assertEqual(elem.getAttribute("isLeaf"), "false")
        self.assertEqual(elem.getAttribute("isActive"), "false")

    def test_owned_operation(self):
        elem = self.xmi_adapator.owned_operation(
            name="arrange_kitchen",
            visibility="public",
            isStatic="false",
            isLeaf="false",
            concurrency="sequential",
            isQuery="false",
            isAbstract="false")

        self.assertEqual(elem.getAttribute("name"), "arrange_kitchen")
        self.assertEqual(elem.getAttribute("xmi:type"), "uml:Operation")

        self.assertEqual(elem.getAttribute("visibility"), "public")
        self.assertEqual(elem.getAttribute("isStatic"), "false")
        self.assertEqual(elem.getAttribute("isLeaf"), "false")
        self.assertEqual(elem.getAttribute("concurrency"), "sequential")
        self.assertEqual(elem.getAttribute("isQuery"), "false")
        self.assertEqual(elem.getAttribute("isAbstract"), "false")

    def test_owned_attribute(self):
        elem = self.xmi_adapator.owned_attribute(
            name="age",
            visibility="public",
            isStatic="false",
            isLeaf="false",
            isReadOnly="false",
            isOrdered="false",
            isUnique="false",
            aggregation="none",
            isDerived="false",
            isID="false")

        self.assertEqual(elem.getAttribute("name"), "age")
        self.assertEqual(elem.getAttribute("xmi:type"), "uml:Property")

        self.assertEqual(elem.getAttribute("visibility"), "public")
        self.assertEqual(elem.getAttribute("isStatic"), "false")
        self.assertEqual(elem.getAttribute("isLeaf"), "false")
        self.assertEqual(elem.getAttribute("isReadOnly"), "false")
        self.assertEqual(elem.getAttribute("isOrdered"), "false")
        self.assertEqual(elem.getAttribute("isUnique"), "false")
        self.assertEqual(elem.getAttribute("aggregation"), "none")
        self.assertEqual(elem.getAttribute("isDerived"), "false")
        self.assertEqual(elem.getAttribute("isID"), "false")

    def test_generalization(self):
        elem = self.xmi_adapator.generalization(
            "AAAAAAFfCb589gvRn9k=", 
            "AAAAAAFfCb3k3guZWwY=",
            visibility="public"
        )

        self.assertEqual(elem.getAttribute("visibility"), "public")
        self.assertEqual(elem.getAttribute("specific"), "AAAAAAFfCb589gvRn9k=")
        self.assertEqual(elem.getAttribute("general"), "AAAAAAFfCb3k3guZWwY=")

    def test_owned_member(self):
        elem = self.xmi_adapator.owned_member(
            name="wings",
            visibility="public",
            isDerived="false"
        )

        self.assertEqual(elem.getAttribute("xmi:type"), "uml:Association")
        self.assertEqual(elem.getAttribute("name"), "wings")
        self.assertEqual(elem.getAttribute("visibility"), "public")
        self.assertEqual(elem.getAttribute("isDerived"), "false")

    def test_owned_end(self):
        elem = self.xmi_adapator.owned_end(
            type="AAAAAAFfCcCaYQxVfw8=",
            visibility="public",
            isStatic="false",
            isLeaf="false",
            isReadOnly="false",
            isOrdered="false",
            isUnique="false",
            aggregation="none",
            isDerived="false",
            isID="false"
        )

        self.assertEqual(elem.getAttribute("xmi-type"), "uml:Association")
        self.assertEqual(elem.getAttribute("type"), "AAAAAAFfCcCaYQxVfw8=")

        self.assertEqual(elem.getAttribute("visibility"), "public")
        self.assertEqual(elem.getAttribute("isStatic"), "false")
        self.assertEqual(elem.getAttribute("isLeaf"), "false")
        self.assertEqual(elem.getAttribute("isReadOnly"), "false")
        self.assertEqual(elem.getAttribute("isOrdered"), "false")
        self.assertEqual(elem.getAttribute("isUnique"), "false")
        self.assertEqual(elem.getAttribute("aggregation"), "none")
        self.assertEqual(elem.getAttribute("isDerived"), "false")
        self.assertEqual(elem.getAttribute("isID"), "false")

    def test_member_end(self):
        elem = self.xmi_adapator.member_end("AAAAAAFfCcDluQy/nQ4=")
        self.assertEqual(elem.getAttribute("xmi:idref"), "AAAAAAFfCcDluQy/nQ4=")

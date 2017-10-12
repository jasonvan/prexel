import unittest
from xml.dom.minidom import Document

from prexel.xmi.adaptor import XMIAdaptor
from prexel.models.diagram import (Diagram,
                                   ClassDiagramPart,
                                   InheritanceDiagramPart,
                                   AggregationDiagramPart)


class TestXMIAdapator(unittest.TestCase):
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

    TODO add more comments

    """
    def setUp(self):
        self.xmi_adapator = XMIAdaptor()

    def test_add_attributes(self):
        package_element = Document().createElement("packagedElement")
        valid_attributes = (
            "attr1",
            "attr2",
            "attr3",
            "attr4",
            "attr5",
        )

        elem_id, elem = self.xmi_adapator._add_attributes(
            package_element, 
            "Model",
            "uml:Model",
            valid_attributes, 
            attr1="attr1",
            attr2="attr2",
            attr3="attr3",
            attr6="attr6"
        )

        self.assertEqual(elem.getAttribute("name"), "Model")
        self.assertEqual(elem.getAttribute("xmi:type"), "uml:Model")
        self.assertEqual(elem.getAttribute("attr1"), "attr1")
        self.assertEqual(elem.getAttribute("attr2"), "attr2")
        self.assertEqual(elem.getAttribute("attr6"), "")

    def test_package_element(self):
        elem_id, elem = self.xmi_adapator.package_element(
            "Model", 
            "uml:Model", 
            visibility="public")

        self.assertEqual(elem.getAttribute("name"), "Model")
        self.assertEqual(elem.getAttribute("xmi:type"), "uml:Model")
        self.assertEqual(elem.getAttribute("visibility"), "public")

        elem_id, elem = self.xmi_adapator.package_element(
            "Kitchen", 
            "uml:Class", 
            visibility="public",
            isAbstract="false",
            isFinalSpecialization="false",
            isLeaf="false",
            isActive="false"
        )

        self.assertEqual(elem.getAttribute("name"), "Kitchen")
        self.assertEqual(elem.getAttribute("xmi:type"), "uml:Class")
        self.assertEqual(elem.getAttribute("visibility"), "public")
        self.assertEqual(elem.getAttribute("isAbstract"), "false")
        self.assertEqual(elem.getAttribute("isFinalSpecialization"), "false")
        self.assertEqual(elem.getAttribute("isLeaf"), "false")
        self.assertEqual(elem.getAttribute("isActive"), "false")

    def test_model_element(self):
        elem_id, elem = self.xmi_adapator.model_element("Model", visibility="public")

        self.assertEqual(elem.getAttribute("name"), "Model")
        self.assertEqual(elem.getAttribute("xmi:type"), "uml:Model")
        self.assertEqual(elem.getAttribute("visibility"), "public")

    def test_class_element(self):
        elem_id, elem = self.xmi_adapator.class_element(
            "Kitchen",
            visibility="public",
            isAbstract="false",
            isFinalSpecialization="false",
            isLeaf="false",
            isActive="false"
        )

        self.assertEqual(elem.getAttribute("name"), "Kitchen")
        self.assertEqual(elem.getAttribute("xmi:type"), "uml:Class")
        self.assertEqual(elem.getAttribute("visibility"), "public")
        self.assertEqual(elem.getAttribute("isAbstract"), "false")
        self.assertEqual(elem.getAttribute("isFinalSpecialization"), "false")
        self.assertEqual(elem.getAttribute("isLeaf"), "false")
        self.assertEqual(elem.getAttribute("isActive"), "false")

    def test_owned_operation(self):
        elem_id, elem = self.xmi_adapator.owned_operation(
            "arrange_kitchen",
            visibility="public",
            isStatic="false",
            isLeaf="false",
            concurrency="sequential",
            isQuery="false",
            isAbstract="false"
        )

        self.assertEqual(elem.getAttribute("name"), "arrange_kitchen")
        self.assertEqual(elem.getAttribute("xmi:type"), "uml:Operation")

        self.assertEqual(elem.getAttribute("visibility"), "public")
        self.assertEqual(elem.getAttribute("isStatic"), "false")
        self.assertEqual(elem.getAttribute("isLeaf"), "false")
        self.assertEqual(elem.getAttribute("concurrency"), "sequential")
        self.assertEqual(elem.getAttribute("isQuery"), "false")
        self.assertEqual(elem.getAttribute("isAbstract"), "false")

    def test_owned_attribute(self):
        elem_id, elem = self.xmi_adapator.owned_attribute(
            "age",
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

import unittest

from prexel.models.diagram import (Diagram,
                                   ClassDiagramPart,
                                   InheritanceDiagramPart,
                                   AggregationDiagramPart)
from prexel.encoders.xmi_encoder import XMIEncoder, XMIDocumentGenerator


class TestXMIEncoder(unittest.TestCase):
    def setUp(self):
        self.maxDiff = 10000

    def test_convert_simple(self):
        simple_class = ClassDiagramPart(
            "Kitchen",
            methods=[
                "arrange_kitchen()",
                "place_floor_cabinet()",
                "place_wall_cabinet()"
            ],
            fields=[
                "field1"
            ]
        )

        expected = """<?xml version="1.0" encoding="UTF-8"?>
<xmi:XMI xmi:version="2.1" xmlns:uml="http://schema.omg.org/spec/UML/2.0" xmlns:xmi="http://schema.omg.org/spec/XMI/2.1">
	<xmi:Documentation exporter="Prexel" exporterVersion="1.0"/>
	<uml:Model name="RootModel" xmi:id="" xmi:type="uml:Model">
		<packagedElement isAbstract="false" isActive="false" isFinalSpecialization="false" isLeaf="false" name="Kitchen" visibility="public" xmi:id="" xmi:type="uml:Class">
			<ownedAttribute aggregation="none" isDerived="false" isID="false" isLeaf="false" isOrdered="false" isReadOnly="false" isStatic="false" isUnique="false" name="field1" visibility="public" xmi:id="" xmi:type="uml:Property"/>
			<ownedOperation concurrency="sequential" isAbstract="false" isLeaf="false" isQuery="false" isStatic="false" name="arrange_kitchen" visibility="public" xmi:id="" xmi:type="uml:Operation"/>
			<ownedOperation concurrency="sequential" isAbstract="false" isLeaf="false" isQuery="false" isStatic="false" name="place_floor_cabinet" visibility="public" xmi:id="" xmi:type="uml:Operation"/>
			<ownedOperation concurrency="sequential" isAbstract="false" isLeaf="false" isQuery="false" isStatic="false" name="place_wall_cabinet" visibility="public" xmi:id="" xmi:type="uml:Operation"/>
		</packagedElement>
	</uml:Model>
</xmi:XMI>
"""

        diagram = Diagram(main=simple_class)
        xmi_encoder = XMIEncoder()
        actual = xmi_encoder.generate(diagram, display_id=False)
        self.assertEqual(expected, actual)

    def test_generate_with_inheritance(self):
        person = ClassDiagramPart("Person", fields=[
            "name",
            "age"
        ])

        inheritance = InheritanceDiagramPart()

        employee = ClassDiagramPart("Employee", fields=[
            "job_title"
        ])

        expected = """<?xml version="1.0" encoding="UTF-8"?>
<xmi:XMI xmi:version="2.1" xmlns:uml="http://schema.omg.org/spec/UML/2.0" xmlns:xmi="http://schema.omg.org/spec/XMI/2.1">
	<xmi:Documentation exporter="Prexel" exporterVersion="1.0"/>
	<uml:Model name="RootModel" xmi:id="" xmi:type="uml:Model">
		<packagedElement isAbstract="false" isActive="false" isFinalSpecialization="false" isLeaf="false" name="Person" visibility="public" xmi:id="" xmi:type="uml:Class">
			<ownedAttribute aggregation="none" isDerived="false" isID="false" isLeaf="false" isOrdered="false" isReadOnly="false" isStatic="false" isUnique="false" name="name" visibility="public" xmi:id="" xmi:type="uml:Property"/>
			<ownedAttribute aggregation="none" isDerived="false" isID="false" isLeaf="false" isOrdered="false" isReadOnly="false" isStatic="false" isUnique="false" name="age" visibility="public" xmi:id="" xmi:type="uml:Property"/>
		</packagedElement>
		<packagedElement isAbstract="false" isActive="false" isFinalSpecialization="false" isLeaf="false" name="Employee" visibility="public" xmi:id="" xmi:type="uml:Class">
			<ownedAttribute aggregation="none" isDerived="false" isID="false" isLeaf="false" isOrdered="false" isReadOnly="false" isStatic="false" isUnique="false" name="job_title" visibility="public" xmi:id="" xmi:type="uml:Property"/>
			<generalization general="" specific="" xmi:type="uml:Generalization"/>
		</packagedElement>
	</uml:Model>
</xmi:XMI>
"""

        diagram = Diagram(employee,
                          parent=person,
                          inheritance=inheritance)

        encoder = XMIEncoder()
        actual = encoder.generate(diagram, display_id=False)
        self.assertEqual(expected, actual)


    def test_generate_with_aggregation(self):
        task_list_diagram = ClassDiagramPart("TaskList", methods=[
            "get_the_tasks()",
            "prioritize()"
        ], fields=["the_tasks"])

        task_list_aggregation = AggregationDiagramPart("the_tasks")
        task_diagram = ClassDiagramPart("Task")

        expected = """<?xml version="1.0" encoding="UTF-8"?>
<xmi:XMI xmi:version="2.1" xmlns:uml="http://schema.omg.org/spec/UML/2.0" xmlns:xmi="http://schema.omg.org/spec/XMI/2.1">
	<xmi:Documentation exporter="Prexel" exporterVersion="1.0"/>
	<uml:Model name="RootModel" xmi:id="" xmi:type="uml:Model">
		<packagedElement isAbstract="false" isActive="false" isFinalSpecialization="false" isLeaf="false" name="TaskList" visibility="public" xmi:id="" xmi:type="uml:Class">
			<ownedAttribute aggregation="none" isDerived="false" isID="false" isLeaf="false" isOrdered="false" isReadOnly="false" isStatic="false" isUnique="false" name="the_tasks" visibility="public" xmi:id="" xmi:type="uml:Property"/>
			<ownedOperation concurrency="sequential" isAbstract="false" isLeaf="false" isQuery="false" isStatic="false" name="get_the_tasks" visibility="public" xmi:id="" xmi:type="uml:Operation"/>
			<ownedOperation concurrency="sequential" isAbstract="false" isLeaf="false" isQuery="false" isStatic="false" name="prioritize" visibility="public" xmi:id="" xmi:type="uml:Operation"/>
		</packagedElement>
		<packagedElement isAbstract="false" isActive="false" isFinalSpecialization="false" isLeaf="false" name="Task" visibility="public" xmi:id="" xmi:type="uml:Class">
			<ownedMember isDerived="false" name="the_tasks" visibility="public" xmi:id="" xmi:type="uml:Association">
				<ownedEnd aggregation="none" isDerived="false" isID="false" isLeaf="false" isOrdered="false" isReadOnly="false" isStatic="false" isUnique="false" type="" visibility="public" xmi:type="uml:Property" xmi:id=""/>
				<ownedEnd aggregation="shared" isDerived="false" isID="false" isLeaf="false" isOrdered="false" isReadOnly="false" isStatic="false" isUnique="false" type="" visibility="public" xmi:type="uml:Property" xmi:id=""/>
				<memberEnd xmi:idref=""/>
				<memberEnd xmi:idref=""/>
			</ownedMember>
		</packagedElement>
	</uml:Model>
</xmi:XMI>
"""

        diagram = Diagram(task_list_diagram,
                          aggregation=task_list_aggregation,
                          aggregated=task_diagram)

        encoder = XMIEncoder()
        actual = encoder.generate(diagram, display_id=False)
        self.assertEqual(expected, actual)

    def test_generate_with_aggregation_with_multiplicity(self):
        employer_diagram = ClassDiagramPart("Employer", fields=[
            "name",
            "age",
            "employees"
        ])

        employees_aggregation = AggregationDiagramPart("employees",
                                                       left_multiplicity="1",
                                                       right_multiplicity="*")
        employee_diagram = ClassDiagramPart("Employee", fields=["position"])

        expected = """<?xml version="1.0" encoding="UTF-8"?>
<xmi:XMI xmi:version="2.1" xmlns:uml="http://schema.omg.org/spec/UML/2.0" xmlns:xmi="http://schema.omg.org/spec/XMI/2.1">
	<xmi:Documentation exporter="Prexel" exporterVersion="1.0"/>
	<uml:Model name="RootModel" xmi:id="" xmi:type="uml:Model">
		<packagedElement isAbstract="false" isActive="false" isFinalSpecialization="false" isLeaf="false" name="Employer" visibility="public" xmi:id="" xmi:type="uml:Class">
			<ownedAttribute aggregation="none" isDerived="false" isID="false" isLeaf="false" isOrdered="false" isReadOnly="false" isStatic="false" isUnique="false" name="name" visibility="public" xmi:id="" xmi:type="uml:Property"/>
			<ownedAttribute aggregation="none" isDerived="false" isID="false" isLeaf="false" isOrdered="false" isReadOnly="false" isStatic="false" isUnique="false" name="age" visibility="public" xmi:id="" xmi:type="uml:Property"/>
			<ownedAttribute aggregation="none" isDerived="false" isID="false" isLeaf="false" isOrdered="false" isReadOnly="false" isStatic="false" isUnique="false" name="employees" visibility="public" xmi:id="" xmi:type="uml:Property"/>
		</packagedElement>
		<packagedElement isAbstract="false" isActive="false" isFinalSpecialization="false" isLeaf="false" name="Employee" visibility="public" xmi:id="" xmi:type="uml:Class">
			<ownedAttribute aggregation="none" isDerived="false" isID="false" isLeaf="false" isOrdered="false" isReadOnly="false" isStatic="false" isUnique="false" name="position" visibility="public" xmi:id="" xmi:type="uml:Property"/>
			<ownedMember isDerived="false" name="employees" visibility="public" xmi:id="" xmi:type="uml:Association">
				<ownedEnd aggregation="none" isDerived="false" isID="false" isLeaf="false" isOrdered="false" isReadOnly="false" isStatic="false" isUnique="false" type="" visibility="public" xmi:type="uml:Property" xmi:id="">
					<lowerValue value="1" xmi:id="" xmi:type="uml:LiteralInteger"/>
					<upperValue value="1" xmi:id="" xmi:type="uml:LiteralInteger"/>
				</ownedEnd>
				<ownedEnd aggregation="shared" isDerived="false" isID="false" isLeaf="false" isOrdered="false" isReadOnly="false" isStatic="false" isUnique="false" type="" visibility="public" xmi:type="uml:Property" xmi:id="">
					<lowerValue value="*" xmi:id="" xmi:type="uml:LiteralUnlimitedNatural"/>
					<upperValue value="*" xmi:id="" xmi:type="uml:LiteralUnlimitedNatural"/>
				</ownedEnd>
				<memberEnd xmi:idref=""/>
				<memberEnd xmi:idref=""/>
			</ownedMember>
		</packagedElement>
	</uml:Model>
</xmi:XMI>
"""

        diagram = Diagram(employer_diagram,
                          aggregation=employees_aggregation,
                          aggregated=employee_diagram)

        encoder = XMIEncoder()
        actual = encoder.generate(diagram, display_id=False)
        self.assertEqual(expected, actual)


class TestXMIDocumentGenerator(unittest.TestCase):
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
        self.xmi_adapator = XMIDocumentGenerator()

    def test_add_attributes(self):
        package_element = self.xmi_adapator.document.createElement("packagedElement")
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

    def test_package_element_with_defaults(self):
        elem = self.xmi_adapator.package_element("uml:Class", "Kitchen")

        self.assertEqual(elem.getAttribute("name"), "Kitchen")
        self.assertEqual(elem.getAttribute("xmi:type"), "uml:Class")

        # Default attributes applied
        self.assertEqual(elem.getAttribute("visibility"), "public")
        self.assertEqual(elem.getAttribute("isAbstract"), "false")
        self.assertEqual(elem.getAttribute("isFinalSpecialization"), "false")
        self.assertEqual(elem.getAttribute("isLeaf"), "false")
        self.assertEqual(elem.getAttribute("isActive"), "false")

    def test_package_element_with_user_specified(self):
        elem = self.xmi_adapator.package_element(
            "uml:Class",
            "Kitchen",
            visibility="private",
            isLeaf="true"
        )

        self.assertEqual(elem.getAttribute("name"), "Kitchen")
        self.assertEqual(elem.getAttribute("xmi:type"), "uml:Class")

        # User-specified attributes
        self.assertEqual(elem.getAttribute("visibility"), "private")
        self.assertEqual(elem.getAttribute("isLeaf"), "true")

        # This attribute wasn't specified so it shouldn't be present
        self.assertNotEqual(elem.getAttribute("isActive"), "true")

    def test_model_element(self):
        elem = self.xmi_adapator.model_element("Model")

        self.assertEqual(elem.getAttribute("name"), "Model")
        self.assertEqual(elem.getAttribute("xmi:type"), "uml:Model")
        self.assertEqual(elem.getAttribute("visibility"), "public")

    def test_class_element(self):
        elem = self.xmi_adapator.class_element("Kitchen")

        self.assertEqual(elem.getAttribute("name"), "Kitchen")
        self.assertEqual(elem.getAttribute("xmi:type"), "uml:Class")

        # Default attributes applied
        self.assertEqual(elem.getAttribute("visibility"), "public")
        self.assertEqual(elem.getAttribute("isAbstract"), "false")
        self.assertEqual(elem.getAttribute("isFinalSpecialization"), "false")
        self.assertEqual(elem.getAttribute("isLeaf"), "false")
        self.assertEqual(elem.getAttribute("isActive"), "false")

    def test_owned_operation(self):
        elem = self.xmi_adapator.owned_operation("arrange_kitchen")

        self.assertEqual(elem.getAttribute("name"), "arrange_kitchen")
        self.assertEqual(elem.getAttribute("xmi:type"), "uml:Operation")

        # Default attributes applied
        self.assertEqual(elem.getAttribute("visibility"), "public")
        self.assertEqual(elem.getAttribute("isStatic"), "false")
        self.assertEqual(elem.getAttribute("isLeaf"), "false")
        self.assertEqual(elem.getAttribute("concurrency"), "sequential")
        self.assertEqual(elem.getAttribute("isQuery"), "false")
        self.assertEqual(elem.getAttribute("isAbstract"), "false")

    def test_owned_attribute(self):
        elem = self.xmi_adapator.owned_attribute("age")

        self.assertEqual(elem.getAttribute("name"), "age")
        self.assertEqual(elem.getAttribute("xmi:type"), "uml:Property")

        # Default attributes applied
        self.assertEqual(elem.getAttribute("visibility"), "public")
        self.assertEqual(elem.getAttribute("isStatic"), "false")
        self.assertEqual(elem.getAttribute("isLeaf"), "false")
        self.assertEqual(elem.getAttribute("isReadOnly"), "false")
        self.assertEqual(elem.getAttribute("isOrdered"), "false")
        self.assertEqual(elem.getAttribute("isUnique"), "false")
        self.assertEqual(elem.getAttribute("aggregation"), "none")
        self.assertEqual(elem.getAttribute("isDerived"), "false")
        self.assertEqual(elem.getAttribute("isID"), "false")

    def test_owned_member(self):
        elem = self.xmi_adapator.owned_member("wings")

        self.assertEqual(elem.getAttribute("xmi:type"), "uml:Association")
        self.assertEqual(elem.getAttribute("name"), "wings")

        # Default attributes applied
        self.assertEqual(elem.getAttribute("visibility"), "public")
        self.assertEqual(elem.getAttribute("isDerived"), "false")

    def test_owned_end(self):
        elem = self.xmi_adapator.owned_end("AAAAAAFfCcCaYQxVfw8=")

        # See owned_end method for an explanation of why "xmi-type" is used
        # instead of "xmi:type"
        self.assertEqual(elem.getAttribute("xmi-type"), "uml:Property")
        self.assertEqual(elem.getAttribute("type"), "AAAAAAFfCcCaYQxVfw8=")

        # Default attributes applied
        self.assertEqual(elem.getAttribute("visibility"), "public")
        self.assertEqual(elem.getAttribute("isStatic"), "false")
        self.assertEqual(elem.getAttribute("isLeaf"), "false")
        self.assertEqual(elem.getAttribute("isReadOnly"), "false")
        self.assertEqual(elem.getAttribute("isOrdered"), "false")
        self.assertEqual(elem.getAttribute("isUnique"), "false")
        self.assertEqual(elem.getAttribute("aggregation"), "none")
        self.assertEqual(elem.getAttribute("isDerived"), "false")
        self.assertEqual(elem.getAttribute("isID"), "false")

    def test_owned_end_shared(self):
        elem = self.xmi_adapator.owned_end("AAAAAAFfCcCaYQxVfw8=",
                                           shared=True)

        self.assertEqual(elem.getAttribute("aggregation"), "shared")

    def test_generalization(self):
        elem = self.xmi_adapator.generalization(
            "AAAAAAFfCb589gvRn9k=",
            "AAAAAAFfCb3k3guZWwY=",
            visibility="public"
        )

        self.assertEqual(elem.getAttribute("visibility"), "public")
        self.assertEqual(elem.getAttribute("specific"), "AAAAAAFfCb589gvRn9k=")
        self.assertEqual(elem.getAttribute("general"), "AAAAAAFfCb3k3guZWwY=")

    def test_member_end(self):
        elem = self.xmi_adapator.member_end("AAAAAAFfCcDluQy/nQ4=")
        self.assertEqual(elem.getAttribute("xmi:idref"), "AAAAAAFfCcDluQy/nQ4=")

    def test_lower_value(self):
        elem = self.xmi_adapator.lower_value("uml:LiteralInteger", "1")

        self.assertEqual(elem.getAttribute("xmi:type"), "uml:LiteralInteger")
        self.assertEqual(elem.getAttribute("value"), "1")

    def test_upper_value(self):
        elem = self.xmi_adapator.lower_value("uml:LiteralUnlimitedNatural", "*")

        self.assertEqual(elem.getAttribute("xmi:type"), "uml:LiteralUnlimitedNatural")
        self.assertEqual(elem.getAttribute("value"), "*")

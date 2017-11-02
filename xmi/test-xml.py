from xml.dom.minidom import Document

document = Document()
xmi = document.createElement('xmi:XMI')
xmi.setAttribute("xmi:version", "2.1")
xmi.setAttribute("xmlns:xmi", "http://schema.omg.org/spec/XMI/2.1")
xmi.setAttribute("xmlns:uml", "http://schema.omg.org/spec/UML/2.0")

documentation = document.createElement("xmi:Documentation")
documentation.setAttribute("exporter", "prexel")
documentation.setAttribute("exporterVersion", "1.0")

uml = document.createElement("uml:Model")
uml.setAttribute("xmi:id", "12345")
uml.setAttribute("xmi:type", "uml:Model")
uml.setAttribute("name", "Model")

packageElement = document.createElement("packageElement")
packageElement.setAttribute("name", "Kitchen")
packageElement.setAttribute("visibility", "public")
packageElement.setAttribute("isAbstract", "false")
packageElement.setAttribute("xmi:type", "Class")

owned_operation = document.createElement("ownedOperation")
owned_operation.setAttribute("xmi:id", "12345")
owned_operation.setAttribute("name", "arrange_kitchen")

packageElement.appendChild(owned_operation)

uml.appendChild(packageElement)
xmi.appendChild(documentation)
xmi.appendChild(uml)

document.appendChild(xmi)
xml = document.toprettyxml(encoding="utf-8")
print(xml.decode('utf-8'))

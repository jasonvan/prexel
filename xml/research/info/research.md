# XML output

* https://en.wikipedia.org/wiki/XML_Metadata_Interchange
* https://en.wikipedia.org/wiki/Unified_Modeling_Language

## Existing tools
* https://github.com/winjer/pyxmi - only seems to work with 1.0 which is quite old. Last commit 7 
years ago.
* https://pypi.python.org/pypi/xmiparser/1.5 - Really just parses XMI, but might be useful for reverse engineering

## XMI spec - http://schema.omg.org/spec/XMI/

* http://www.omg.org/spec/XMI/2.5.1/ - Current - June, 2015
* http://www.omg.org/spec/XMI/2.4.2/ - Formal ISO spec - April, 2014
* http://www.omg.org/spec/XMI/2.4.1/ - August, 2011
* http://schema.omg.org/spec/XMI/2.1/ - September, 2005

## UML spec - http://schema.omg.org/spec/UML/

* http://www.omg.org/spec/UML/2.5/ - Current - June, 2015
* http://www.omg.org/spec/UML/2.4.1/ - Formal ISO spec - August, 2011
* http://www.omg.org/spec/UML/2.2/ - Supported by IBM - February, 2009
* http://schema.omg.org/spec/UML/2.0/ - Supported by StarUML - July, 2005
* http://www.omg.org/spec/UML/20110701/UML.xmi - contains stuff like packagedElement, etc

## Support

"Full" list of tools from this url - https://en.wikipedia.org/wiki/List_of_Unified_Modeling_Language_tools

### StarUML
* XMI 2.1 based on UML 2.0 metamodel
	* Import available via plugin - https://blog.staruml.io/2015/03/05/xmi-extension/

### IBM
* XMI - not specified
* UML - 2.1/2.2 
	* https://www.ibm.com/support/knowledgecenter/SS8PJ7_9.6.1/com.ibm.xtools.modeler.doc/topics/timportexportmodels.html

### ArgoUML
* Support but for very old standard
	* UML 1.3/1.4 stored in XMI 1.0,1.1,1.2
	* http://argouml.stage.tigris.org/faqs/users.html#xmib_link

### PlantUML - http://plantuml.com/xmi
* Can export XMI, but nothing found on importing XMI

### UMLet
* Doesn't support XMI import, to much work to support 
	* https://github.com/umlet/umlet/issues/104

### Astah - http://astah.net/
* XMI version 2.1
	* Import available via a plugin - http://astah.net/features/xmi-plugin

### Enterprise Architect
* UML 1.3 - 2.X via (XMI 1.0 - 2.1)
	* http://www.sparxsystems.com/enterprise_architect_user_guide/10/projects_and_teams/importxmi.html

### UML Designer - http://www.umldesigner.org/
* Can but doesn't specify which version of XMI
	* http://www.umldesigner.org/tutorials/tuto-import-model.html

### Eclipse UML2 Tools
* Not clear, but looks like UML 2.X as a XMI 2.1 file
	* https://www.eclipse.org/forums/index.php/t/150893/ 

### MagicDraw
* Supports UML2 via XMI 2.1
	* https://docs.nomagic.com/display/MD182/Importing+data+from+other+UML+tools+and+formats

### Visio
* Doesn't appear to support import of XMI
	* http://visguy.com/vgforum/index.php?topic=1256.0

### Altova
* Supports XMI 2.1 - 2.4.1 for UML 2.0, 2.1.2, 2.2, 2.3, 2.4.1
	* https://www.altova.com/umodel/advanced

## Meeting notes

## Next Actions

* Research are people are using UML in the agile process? Where does PREXEL fit in to this?
    
* Allow for multiple subclasses which will be comma-delimited. [Interpreter, Encoders, Lexer, Regex]
    * Interpreter will need to be updated to loop over subclass with optional aggregation multiple times [Interpreter]
    * Encoders will need to be updated to handle multiple main classes
* Right now now single-line and multi-line add aggregated values in different orders [Interpreter]
* Need to throw an exception if an ignored character is used, this needs to be handled by the plugin [Lexer]
* need to handle "S" character, and create class variable in source code [Interpreter]
* Merge multiple PREXEL strings together. [Encoders]
* Plan out XML fragment implementation [XML Code]

* Comment/Clean up encoder code/tests [Code Quality]
* Search for all TODOs in project [Code Quality]

## Backlog

### Code Quality

### Interpreter

* Review aggregation method. It might be more clear to break this up into 
separate methods
* Review evaluate method again
* Use the left multiplicity value for aggregation
* Use the right multiplicity value for aggregation
* Allow for multiple loops of code inside of evaluate method
* Optional
    * Write out current grammer for parser
    * Define a comprehensive grammar
    * Read up on AST
    * Put tokens into AST if needed
    * Generate diagram objects from AST

### Lexer

* Read up on AST
* Add the following self aggregation, need to determine a shorthand for this
    <>-----
    <------
* Add dependence
    * need dialog box to decide what type of dependence

### Encoders

* Source code - add comment to aggregation, noting the Class name aggregated,
this is immediately obvious since Python is not typed
    
### Plugin

* Update the option to generate a class to use view.show_popup_menu
* Allow user the option to specify if they want pretty-print or source code, 
both, or neither, when running the prexel command

* I’ve also been thinking a lot about the “need” to synchorize between 
generated classes, XML fragment, and pretty-printed diagrams. 
I believe we still need to synchronize the XML fragment and pretty-printed 
diagram, but I question whether we need to keep t

### XML Code

* Determine more tasks 
* XMIAdaptor - handles the conversion of a Diagram object in and out of XMI
* Fragment aggregation code
* Create ASCII version of UML for entire project
* Research if anyone is doing aggregation/inheritance first UML models. These would focus on 
one of these relationships as the main diagram form and other relationships would only be annotated.
* Validation of fragments
* Review presentation of large diagram for all classes in the project 

### Planning

* https://drive.google.com/file/d/0B9_FGv0nRq5hSGJlbm5WVC1BMG8/view?usp=sharing
* Research the structure of XMI
    * https://www.ibm.com/developerworks/library/x-wxxm24/index.html
    * http://www.omg.org/spec/DD/1.0/
* Review Sublime text's plugin architecture
    * https://stackoverflow.com/questions/30443820/insert-text-into-view-in-sublime-3-api
    * https://cnpagency.com/blog/creating-sublime-text-3-plugins-part-1/
    * https://cnpagency.com/blog/creating-sublime-text-3-plugins-part-2/
    * http://techsideonline.com/sublime-text-3-plugin/
    * https://www.sublimetext.com/docs/3/api_reference.html#sublime.Edit
    * https://stackoverflow.com/questions/30443820/insert-text-into-view-in-sublime-3-api
    * /Applications/Sublime Text.app/Contents/MacOS/Packages/default

## Design

### Four top level packages in the project:

**models** - This package contains the domain objects for this plugin. The main class
is the Diagram class. This represents a single diagram element inside of a selection of PREXEL
text. 

For instance the PREXEL below contains two diagram elements.

    """
    |Kitchen color square_feet show_kitchen()  # diagram element 1
    
    |Employee  # diagram element 2
    |job_title
    
**parsers** - This manages the parsing and interpretation of easy-entry PREXEL. 
The parser creates Diagram objects for the easy-entry PREXEL. These are then processed
by the classes inside of the XML package into XMI fragments.

**xml** - This manages the conversion of Diagram objects to and from XMI fragments.
It also handles the aggregation of all fragments for the project into one XML file as well
as validation.

**encoders** - The classes in this package are responsible for taking a Diagram object
and encoding it into strings for output in the editor. There are two output types:
Source Code and Pretty printing.

#### Prexel conversion process

[Plugin gets selected string] **=>** [Parser parses string in Diagram objects] **=>** [XMI Adapator converts
Diagram objects in XMI fragments] **=>** [Diagram objects are encoded into Pretty-printed and Source code
output] **=>** [Plugin takes the Pretty-printed and source code and outputs them]

## Meeting Notes

### Demo

* examples.py
* README

### Syntax

This doesn't allow for aggregation

    |Kitchen arrange_kitchen() place_floor_cabinet() place_wall_cabinet() << Room

This does

    |Kitchen << Room color square_feet show_kitchen() <>*-cupboards--1> Cupboard open()"

Or perhaps this would be best. That way we specify values on the Room

    |Room >> Kitchen color square_feet show_kitchen() <>*-cupboards--1> Cupboard open()"

This way parent classes could have fields and methods

    |Room width height >> Kitchen color square_feed show_kitchen() <>*-cupboards--1> Cupboard open()

### Usage in docstrings

I didn't include the constraint PREXEL to have to be inside of docstrings
this way it can be used in other files, for example I used it when updating the 
examples inside of the README, which is a markdown file. 

Plus it is way faster to type.

### Prep for submission

* Use dropbox for source?
* remove git repo for submitted zip as it has reference to github

### Improvements

* Can't handle multiple inheritance right now
* Can't handle multiple aggregation right now
* Can't handle self aggregation right now
* Can't handle static "S"
* need to figure out a way to handle merging multiple diagrams

## Backlog

### Next Actions

* Search for all TODOs in project
* Comment/Clean up interpreter code/tests
* Comment/Clean up lexer code/tests
* Comment/Clean up encoder code/tests

* Update interpreter to agreed upon structure
    * need to handle "S" character, and create class variable in source code
    * need to determine how we want the aggregated value added to the aggregator

* need to add more describitive messages to interpreter
right now single-line and multi-line do it in a different order
* Allow for multiple loops of code inside of evaluate method
    
### Interpreter

* Comment source and test classes [NA]
* Create a default value from aggregation if not specified [NA]
* Use the left multiplicity value for aggregation
* Use the right multiplicity value for aggregation
* Optional
    * Write out current grammer for parser
    * Define a comprehensive grammar
    * Read up on AST
    * Put tokens into AST if needed
    * Generate diagram objects from AST

### Lexer

* Clean up evaluate method [NA]
* Comment source and test classes [NA]
* Need to add the usage of regex tester
    <>-----
    <------

* Handle Dependence

### Encoders

* Source code - add comment to aggregation, noting the Class name aggregated,
this is immediately obvious since Python is not typed
    
### Plugin

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

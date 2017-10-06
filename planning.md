## Next Actions

* Import simple sample xmi into other tools and see how they display. Can we use them
    * If they don't do what we want, perhaps we should write our own
    * Make export possible to other tools ( using valid UML 2.0 and XMI 2.1 ), but also generate our own
    * We aren't trying to implement everything
* Look into the display of diagram
    * Classes as a circle with all the connections together
    * Aggregation with a numbered box and numbered correspoding box
* Add space between class and first method, confirm this is accurate according to PEP8
* Check into issue tracker
* Undo
    * Comment and clean up
    * Move common code for UndoUmlCommand and ReverseUmlCommand to one method
    * Need to figure out a way to handle undoing when two prexel strings are the same. It always finds the first one in the file first

## Backlog

* Plan out XML fragment implementation [XML Code]
* Allow for multiple subclasses which will be comma-delimited. [Interpreter, Encoders, Lexer, Regex]
    * Interpreter will need to be updated to loop over subclass with optional aggregation multiple times [Interpreter]
    * Encoders will need to be updated to handle multiple main classes
* Right now now single-line and multi-line add aggregated values in different orders [Interpreter]
* Need to throw an exception if an ignored character is used, this needs to be handled by the plugin [Lexer]
* need to handle "S" character, and create class variable in source code [Interpreter]
* Merge multiple PREXEL strings together. [Encoders]

* Comment/Clean up encoder code/tests [Code Quality]
* Search for all TODOs in project [Code Quality]

* Research are people are using UML in the agile process? Where does PREXEL fit 

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
this is not immediately obvious since Python is not typed
    
### Plugin


### XML Code

* Determine more tasks 
* XMIAdaptor - handles the conversion of a Diagram object in and out of XMI
* Fragment aggregation code
* Create ASCII version of UML for entire project
* Research if anyone is doing aggregation/inheritance first UML models. These would focus on 
one of these relationships as the main diagram form and other relationships would only be annotated.
* Validation of fragments
* Review presentation of large diagram for all classes in the project 

### Resources

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

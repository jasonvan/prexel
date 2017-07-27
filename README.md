# Prexel

# Instruction

Currently there is a test suite available to test the code. This can be found at:

    prexel/plugin/tests/

Running the test can be done from the command line, with the following command:

    python3 -m unittest prexel/plugin/tests/encoders/test_pretty_print_encoder.py
    python3 -m unittest prexel/plugin/tests/encoders/test_source_code_encoder.py 
    python3 -m unittest prexel/plugin/tests/parser/test_lexer.py
    python3 -m unittest prexel/plugin/tests/test_regex.py

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

### Plugin - prexel.py

The main sublime text specific code is found inside of prexel.py. This file
manages all of the interaction with the sublime plugin API to determine what text
to process, file creation, outputting formatted text, etc.

#### Prexel conversion process

[Plugin gets selected string] **=>** [Parser parses string in Diagram objects] **=>** [XMI Adapator converts
Diagram objects in XMI fragments] **=>** [Diagram objects are encoded into Pretty-printed and Source code
output] **=>** [Plugin takes the Pretty-printed and source code and outputs them]

## Progress

Currently the bulk of the completed code is inside the **encoders** and **parsers** packages.
There is still work to be done in both these packages as can be noted in the task list
below. In terms of **models**, a basic Diagram object has been created, but will most
likely be expanded in the future. The classes inside of the **XML** package 
have not been written yet.The **plugin** code has a skeleton class setup, but is not
currently hooked up to the parsers or encoders. 

### Next Step

The next step of the project is to finish up the parsers code and then have the
plugin class utilize this to process easy-entry code into a Diagram object. This 
Diagram object will be passed directly to the encoders for output the editor. Once the 
XML code has been written, the parser will pass the Diagram object to an adaptor class
that will handle convertting it to XMI fragments.


## Tasks

* Parser
    * Lexer
        * Comment test classes
        * Handle aggregation
        * Handle Dependence
        * Handle inheritance
    * Interpreter
        * [DETERMINE TASKS]
* Encoders
    * Pretty Print
        * Inheritance encoding
        * Dependence encoding
        * Aggregation encoding
    * Source Code 
        * [DETERMINE REMAINING TASKS]
* Plugin
    * [DETERMINE MORE TASKS]
    * Create new file for source code
    * Split prexel entry on newlines
    * Allow user the option to specify if they want pretty-print or source code, both, or neither,
    when running the prexel command
* XML Package
    * [DETERMINE MORE TASKS]
    * XMIAdaptor - handles the conversion of a Diagram object in and out of XMI
    * Fragment aggregation code
    * Validation of fragments

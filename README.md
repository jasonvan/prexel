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

1) **models** - This package contains the domain objects for this plugin. The main class
is the Diagram class. This represents a single diagram element inside of a selection of PREXEL
text. 

For instance the PREXEL below contains two diagram elements.

    """
    |Kitchen color square_feet show_kitchen()  # diagram element 1
    
    |Employee  # diagram element 2
    |job_title

2) **encoders** - The classes in this package are responsible for taking a Diagram object
and encoding it into strings for output in the editor. There are two output types:
Source Code and Pretty printing.

3) **xml** - This manages the conversion of domain objects to XMI fragments, as
well as the aggregation of all fragments for the project into one XML file. This 
also manages the validation of the fragments against the code.

4) **parsers** - This manages the parsing and interpretation of easy-entry PREXEL. 
The parser creates Diagram objects for the easy-entry PREXEL. These are then processed
by the classes inside of the XML package into XMI fragments.

### Plugin - prexel.py

The main sublime text specific code is found inside of prexel.py. This file
manages all of the interaction with the sublime plugin API to determine what text
to process, file creation, outputting formatted text, etc.

## Progress

Currently the bulk of the completed code is inside the encoders and parsers packages.
There is still work to be done in both these packages and can be noted in the task like
below. The 
represent the most complex part.

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
    * XMIAdaptor - handles the conversion of a Diagram object in and out of XMI
    * Fragment aggregation code
    * Validation of fragments

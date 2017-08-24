# Prexel

## Installation

The plugin should be installed inside of the Sublime Text packages folder. Once inside Sublime text will automatically load the plugin, **SO YOU'RE DONE**.

**Windows**

	%APPDATA%\Sublime Text 3\Packages

**MAC/OSX**

	~/Library/Application Support/Sublime Text 3/Packages

**LINUX**

	~/.config/sublime-text-3/Packages

## Usage

Place the cursor in a line with a PREXEL string (**SEE next section for examples**) and press CTRL+SHIFT+G (Windows/Linux) or COMMAND+SHIFT+G (MAC) to expand to a pretty-printed version.

**Source Code Generation**

When expanding PREXEL, you have the option of generating source code for the diagram. You will see a dialog box at the bottom of the editor when expanding to pretty-printed version, which also you specifiy if you want source code generated or not.

## Entry examples

Below are some examples of easy entry for Prexel. Using easy entry, the developer
can quickly create UML fragments inside of source file comments. It will also generate source code based on the UML diagrams generated.

### Example 1 - Basic Class

Easy-entry single-line:

    |Kitchen arrange_kitchen() place_floor_cabinet() place_wall_cabinet()

Easy-entry multi-line:

    |Kitchen
    |arrange_kitchen()
    |place_floor_cabinet()
    |place_wall_cabinet()

Pretty-printed UML generated:
     _____________________ 
    |       Kitchen       |
    |---------------------|
    |arrange_kitchen()    |
    |place_floor_cabinet()|
    |place_wall_cabinet() |
    |_____________________|
    
Source code generated:

    class Kitchen:
        def arrange_kitchen(self):
            pass

        def place_floor_cabinet(self):
            pass

        def place_wall_cabinet(self):
            pass


### Example 2 - Multiple Classes with Inheritance

Easy-entry single-line:
    
    |Person << Employee name age

Easy-entry multi-line:

    |Person << Employee
    |name
    |age

Pretty-printed UML:

     ________ 
    |Employee|
    |________|
    ∆
    |______ 
    |Person|
    |------|
    |name  |
    |age   |
    |______|

Source code generated (each class in its own file):

    class Employee:
        pass

    class Person(Employee):
        def __init__(self, name, age):
            self.name = name
            self.age = age

### Example 3 - Aggregation

Easy-entry single-line:

    |Airplane color weight <>-wings-> Wing

Easy-entry multi-line:

    |Airplane <>-wings-> Wing
    |color
    |weight

Pretty-printed UML:
     ________              ____ 
    |Airplane|<>-wings--->|Wing|
    |--------|            |____|
    |color   |                  
    |weight  |                  
    |wings   |                  
    |________|                  

Source code generated (each class in its own file):

    class Airplane:
        def __init__(self, color, weight, wings):
            self.color = color
            self.weight = weight
            self.wings = wings

    class Wing:
        pass
          
### Example 4 - Multiplicity

Easy-entry single-line:

    |Employer name age <>1-employees--*> Employee position

Easy-entry multi-line (in multi-line, Employee can't have fields)

    |Employer <>1-employees--*> Employee
    |name
    |age


Pretty-printed UML:

     _________                    ________ 
    |Employer |<>1-employees---*>|Employee|
    |---------|                  |--------|
    |name     |                  |position|
    |age      |                  |________|
    |employees|                            
    |_________|                            

     _________                    ________ 
    |Employer |<>1-employees---*>|Employee|
    |---------|                  |________|
    |employees|                            
    |name     |                            
    |age      |                            
    |_________|                            

Source code generated (each class in its own file):

    class Employer:
        def __init__(self, name, age, employees):
            self.name = name
            self.age = age
            self.employees = employees

    class Employee:
        def __init__(self, position):
            self.position = position


### Example 5 - Aggregation and Inheritance 

Easy-entry single-line:

    |Kitchen << Room color square_feet show_kitchen() <>*-cupboards--1> Cupboard open()

Easy-entry multi-line (in multi-line, Cupboard can't have fields)

    |Kitchen << Room <>*-cupboards--1> Cupboard
    |color
    |square_feet
    |show_kitchen()

Pretty-printed UML:
     ____ 
    |Room|
    |____|
    ∆
    |______________                    ________ 
    |   Kitchen    |<>*-cupboards---1>|Cupboard|
    |--------------|                  |--------|
    |color         |                  |open()  |
    |square_feet   |                  |________|
    |cupboards     |                            
    |show_kitchen()|                            
    |______________|                            

Source code generated (each class in its own file):

    class Room:
        pass

    class Kitchen(Room):
        def __init__(self, color, square_feet, cupboards):
            self.color = color
            self.square_feet = square_feet
            self.cupboards = cupboards

        def show_kitchen(self):
            pass

    class Cupboard:
        def open(self):
            pass

## Tests

Currently there is a test suite available to test the code. This can be found at:

    prexel/plugin/tests/

Running the test can be done from the command line, with the following command:

    python3 -m unittest prexel/plugin/tests/test_pretty_print_encoder.py
    python3 -m unittest prexel/plugin/tests/test_source_code_encoder.py 
    python3 -m unittest prexel/plugin/tests/test_lexer.py
    python3 -m unittest prexel/plugin/tests/test_interpreter.py
    python3 -m unittest prexel/plugin/tests/test_regex.py



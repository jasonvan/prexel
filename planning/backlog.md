# Backlog

## Convert easy-entry UML comments into pretty-printed version

### Planning

* Create class model for prexel plugin [ IN PROGRESS ]
    * https://drive.google.com/file/d/0B9_FGv0nRq5hSGJlbm5WVC1BMG8/view?usp=sharing
* Research the structure of XMI
    * https://www.ibm.com/developerworks/library/x-wxxm24/index.html
    * http://www.omg.org/spec/DD/1.0/
* Review Sublime text's plugin architecture

### Implementation

#### Convert easy-entry into an XML representation of the fragment

* Write code to process the different easy-entry strings [ IN PROGRESS ]
    * Create a test setup
    * Determine regex that is need for processing the easy-entry strings
    * Add Linux and Windows .sublime-keymap files
* Write code to generate XMI

#### Use XML fragment to generate pretty-printed version of the diagram

[TODO:Determine tasks]

#### Create entire XML version of UML for entire project

[TODO:Determine tasks]

#### Create an ASCII version of UML and save to file

[TODO:Determine tasks]

## Diagram Generation

* Research if anyone is doing aggregation/inheritance first UML models. These would focus on 
one of these relationships as the main diagram form and other relationships would only be annotated.

## Misc

* Take a look at https://www.genmymodel.com/staruml
* Update README for project
* I could see the benefit of also going from pretty-printed to easy-entry. For instance
if you wanted to make a major update to the pretty-printed UML it might easier to 
get it back into easy-entry, make your additions, and recreate the pretty-printed UML

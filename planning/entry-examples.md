# Entry examples

Below are some examples of easy entry for Prexel. Using easy entry, the developer
can quickly create UML fragments inside of the source file.

## Examples

### Example 1 - Basic Class

Easy-entry code:

    """
        
    |Kitchen
    |arrange_kitchen()
    |place_floor_cabinet()
    |place_wall_cabinet()
        
    """

Pretty-printed UML generated:

    """
     _____________________
    |       Kitchen       |
    |---------------------|
    |arrange_kitchen()    |
    |place_floor_cabinet()|
    |place_wall_cabinet() |
    |_____________________|
        
    
    """

Source code generated:

    class Kitchen:
        def arrange_kitchen(self):
            pass
            
        def place_floor_cabinet(self):
            pass
            
        def place_wall_cabinet(self):
            pass


### Example 2 - Multiple Classes with inheritence

Easy-entry code:

    """
        
    |Person
    |name
    |age
     
    |Employee
    |job_title
        
    Person
    ^
    Employee
        
    """

Pretty-printed UML:

    """
     __________
    |  Person  |
    |----------|
    |name      |
    |age       |
     ----------
          ^    
     ____________ 
    |  Employee  |
    |------------|
    |job_title   |
     ------------  
        
    """

Source code generated:

    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age
        
    class Employee(Person):
        def __init__(self, job_title):
            self.job_title = job_title
            

### Example 3 - Dependence

Easy-entry code:

    """
    
    Style->XCabinet
    
    |Style
    |get_cabinets()
     
    """
    
Pretty-printed UML:

    """
     _______________ 
    |     Style     |      ____________
    |---------------|---->|  XCabinet  |
    |get_cabinet()  |      ------------
     ---------------
     
     """

Source code generated:

    class Style:
        def get_cabinet():
            return XCabinet()
            
    class XCabinet:
        pass

### Example 3 - Aggregation

Easy-entry code:

    """
        
    Airplane<>-wings->Wing
        
    """

Pretty-printed UML:

    """
                          ________
    Airplane<>---wing--->|  Wing  |
                          --------
    """

Source code generated:

    class Airplane:
        def __init__(self, wing):
            self.wing = wing
        
    class Wing:
        pass
          

### Example 4 - Aggregation and Inheritence 

Easy-entry code:

    """
        
    Kitchen<>->XCabinet
        
    =XCabinet=
    ^
    AntiqueXCabinet|ModernXCabinet
    
        
    |AntiqueXCabinet
    |place_antique_x_cabinet()
        
    |ModernXCabinet
    |place_modern_x_cabinet()
        
    """ 

Pretty-printed UML:

                       _________________
    Kitchen<>-------->|     XCabinet    |
                      | << interface >> |
                       -----------------
     _________________________ ^ ________________________
    |    AntiqueXCabinet      | |    ModernXCabinet      |
    |-------------------------| |------------------------|
    |place_antique_x_cabinet()| |place_modern_x_cabinet()|
     -------------------------   ------------------------
     
    """

Source code generated:

    
    class Kitchen:
        def arrange_kitchen(self):
            pass
            
        def place_floor_cabinet(self):
            pass
            
        def place_wall_cabinet(self):
            pass

## TODOs

* How should we denote abstract classes and interfaces
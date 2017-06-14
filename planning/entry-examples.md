# Entry examples

Below are some examples of easy entry for Prexel. Using easy entry, the developer
can quickly create UML fragments inside of source file comments. It will also generate source code based on the UML diagrams generated.

## Example 1 - Basic Class

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
     --------------------- 
        
    
    """

Source code generated:

    class Kitchen:
        def arrange_kitchen(self):
            pass
            
        def place_floor_cabinet(self):
            pass
            
        def place_wall_cabinet(self):
            pass


## Example 2 - Multiple Classes with Inheritance

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
            

## Example 3 - Dependence

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

## Example 4 - Aggregation

Easy-entry code:

    """
        
    Airplane<>-wings->Wing
        
    """

Pretty-printed UML:

    """
     __________               ________
    | Airplane |<>---wing--->|  Wing  |
     ----------               --------
    """

Source code generated:

    class Airplane:
        def __init__(self, wing):
            self.wing = wing
        
    class Wing:
        pass
          
          
## Example 5 - Association

Easy-entry code:

    """
        
    Employer--Employee
        
    """

Pretty-printed UML:

    """
     __________       __________
    | Employer |-----| Employee |
     ----------       ----------
     
    """

Source code generated:

    class Employer:
        def __init__(self, employee):
            self.employee = employee
        
    class Employee:
        def __init__(self, employer):
            self.employer = employer

## Example 6 - Multiplicity

Easy-entry code:

    """
        
    Employer<>1-*>Employee
        
    """

Pretty-printed UML:

    """
     __________ 1     *  __________
    | Employer |<>----->| Employee |
     ----------          ----------
     
    """

Source code generated:

    class Employer:
        def __init__(self, employees):
            self.employees = []
        
    class Employee:
        pass

## Example 7 - Aggregation and Inheritance 

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

    """
     _________             _________________
    | Kitchen |<>-------->|     XCabinet    |
     ---------            | << interface >> |
                           -----------------
     _________________________ ^ ________________________
    |    AntiqueXCabinet      | |    ModernXCabinet      |
    |-------------------------| |------------------------|
    |place_antique_x_cabinet()| |place_modern_x_cabinet()|
     -------------------------   ------------------------
     
    """

Source code generated:

    
    import abc.ABCMeta
        
    class Kitchen:
        def __init__(self, xcabinet):
            self.xcabinet = xcabinet
            
        def arrange_kitchen(self):
            pass
            
        def place_floor_cabinet(self):
            pass
            
        def place_wall_cabinet(self):
            pass
            
    class XCabinet(metaclass=ABCMeta):
        pass
        
    class AntiqueXCabinet(XCabinet):
        def place_antique_x_cabinet():
            pass
        
    class ModernXCabinet(XCabinet):
        def place_modern_x_cabinet():
            pass

## TODOs

* How should we denote abstract classes and interfaces

## Ideas

* I could see the benefit of also going from pretty-printed to easy-entry. For instance
if you wanted to make a major update to the pretty-printed UML it might easier to 
get it back into easy-entry, make your additions, and recreate the pretty-printed UML

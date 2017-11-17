import os
import re
from utils import Persistence

mydir = "/Users/Jenessa/Documents/Jason/Boston-University/Grad Assistant/prexel"

"""
===#
 ____ 
|Room|
|____|
∆
|____________                ______ 
| LivingRoom |<>-windows--->|Window|
|------------|              |______|
|size        |                      
|height      |                      
|open_windows|                      
|windows     |                      
|____________|                      
===#

"""

regex = re.compile(r"(===#)(.*?)(===#)", re.DOTALL)

persistence = Persistence()

for dirpath, _, filenames in os.walk(mydir):
    for file in filenames:
        if file != "__init__.py" and file == "test-walking.py":
            file_path = os.path.join(dirpath, file)
            with open(file_path) as file:
                value = regex.findall(file.read())[0][1]
                print(persistence._generate_hashcode(value))

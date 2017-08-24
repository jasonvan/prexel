"""

|Kitchen << Room

|Kitchen arrange_kitchen() place_floor_cabinet() place_wall_cabinet()

|Kitchen
|arrange_kitchen()
|place_floor_cabinet()
|place_wall_cabinet()

|Person << Employee name age

|Person << Employee
|name
|age

|Airplane color weight <>-wings-> Wing

|Airplane <>-wings-> Wing
|color
|weight

|Employer name age <>1-employees--*> Employee position

|Employer <>1-employees--*> Employee
|name
|age

|Tasklist <>-the_tasks--*> Task
|get_the_tasks()
|prioritize()

|Kitchen << Room color square_feet show_kitchen() <>*-cupboards--1> Cupboard open()

|Kitchen << Room <>*-cupboards--1> Cupboard
|color
|square_feet
|show_kitchen()

|Kitchen <<
"""


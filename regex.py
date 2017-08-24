import re

"""
|Kitchen << Room color square_feet show_kitchen() <>*-cupboards--1> Cupboard open()

|Kitchen
|color
|square_feet
|show_kitchen()

|Tasklist <>-the_tasks--*> Task
|get_the_tasks()
|prioritize()

|Kitchen << Room

"""

REGEX = {
    "class_name": re.compile(r'^[A-Z]\w*$'),
    "method_signature": re.compile(r'^([^(){}]+)\((.*)\)$'),
    "aggregation": re.compile('^<>([\d*]?)-+(\w*)-*([\d*]?)>$'),
    "inheritance": re.compile('^<<$')
}

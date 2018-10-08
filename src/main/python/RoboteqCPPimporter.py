#!/usr/bin/python
import sys
sys.path = ["../"] + sys.path   #set sys in order to be able to locate header fileself.

import CppHeaderParser

try:
    cppHeader = CppHeaderParser.CppHeader("Constants.h")
except CppHeaderParser.CppParseError as e:
    print(e)
    sys.exit(1)

print("CppHeaderParser view of %s"%cppHeader)

RoboteqCommandDict = dict()

print("\n#defines are:")
for define in cppHeader.defines:
    command = define.split(' ')
    if len(command) == 2:
         #TODO try to optimize this code to perform proper data access for fast operation.
         #TODO there is definitely a better way to do the string formatting in python
         #The formatting of the print statement comes from the round about way that values are #defined in the Roboteq CPP install_dependencies
         #Their identity string is defined as a decimal representation of their HEX valueself.
         #we need to do all of that conversion here in order to make this work with Roboteq Command Generator.
        RoboteqCommandDict[command[0]] = '${:02x}'.format(int(command[1])) #using .format() instead of fstring to match formatting in RoboteQ CPP API
print(RoboteqCommandDict)

####Defines are formated as keys that will have to be formatted like '${:02X}'.format(value)

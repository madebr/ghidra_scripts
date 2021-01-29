# Convert a string array to an enum

# Convert selected string arrays to an enum.

#@category Data Types

import re
import sys

def error(msg):
  println(msg)
  sys.exit(1)
  
  
def format_array(array):
  nb_elements = array.getDataType().getNumElements()
  element_size = array.getDataType().getElementLength()
  strings = []
  for i in range(nb_elements):
    subaddr = array.getComponentAt(element_size * i).getValue()
    if not isinstance(subaddr, ghidra.program.model.address.Address):
      error("Not an address")
    s_element = currentProgram.getListing().getDataAt(subaddr)
    if s_element.getDataType().name != "string":
      error("element of array[{}] at 0x{} is not a string".format(i, subaddr))
    strings.append(s_element.getValue())
  # print(strings)
  strings_nice = ["0x{:02x}_{}".format(i, s) for i, s in enumerate(strings)]
  strings_nice = [re.subn("[ '-.:]", "_", name)[0] for name in strings_nice]
  # print(strings_nice)
  return strings_nice
  
    #subaddr = j_data.getComponentAt(4*i).getValue()
    #s = currentProgram.getListing().getDataAt(subaddr)
    #d.append(s.getValue())


def create_enum_from_array(array, name, prefix):
  dataTypeManager = currentProgram.getDataTypeManager()
  new_enum = ghidra.program.model.data.EnumDataType(name, 4)
  for i, n in enumerate(array):
    new_enum.add(prefix + n, i)
  return new_enum


if not currentProgram:
  error("This script is meant to be run with an active program")
  
if not currentSelection:
  error("This script needs a selection")

for data in currentProgram.getListing().getCompositeData(currentSelection.minAddress, True):
  if data.getAddress() >= currentSelection.maxAddress:
    break
  # data = currentProgram.getListing().getDataAt(a0)
  if data.isArray():
    println("{} is an array".format(data))
    array = format_array(data)
    name = askString("String array detected at 0x{}".format(data.getAddress()), "{} elements. Name?".format(len(array)))
    prefix = askString("String array detected at 0x{}".format(data.getAddress()), "prefix?")
    datatype = create_enum_from_array(array, name=name, prefix=prefix)
    currentProgram.getDataTypeManager().addDataType(datatype, None)
  else:
    println("{} is NOT an array".format(data))

sys.exit(0)

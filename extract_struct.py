#Extract data at pointer to a python structure
#@author Me
#@category Selection
#@keybinding 
#@menupath 
#@toolbar 

currentListing = currentProgram.listing

def parse_item(item):
  if item is None:
    return None
  item_datatype = item.dataType
  if item.isStructure():
    #print([item_datatype.getComponent(i).getFieldName() for i in range(item.getNumComponents()) ])
    return { item_datatype.getComponent(i).getFieldName(): parse_item(item.getComponent(i)) for i in range(item.numComponents) }
  elif item.isArray():
    return [ parse_item(item.getComponent(i)) for i in range(item.numComponents) ]
  dt_str = str(item_datatype)
  if dt_str == "char *":
    d = currentListing.getDefinedDataAt(item.getValue())
    if d:
      return d.value
    else:
      print("err at {}".format(item.getValue()))
      return None
  elif item.isPointer():
    if item.getValue().getUnsignedOffset() == 0:
      return None
    else:
      return parse_item(currentListing.getDefinedDataAt(item.getValue()))
  else:
    item_value = item.getValue()
    if hasattr(item_value, "value"):
        return item_value.value
    else:
        return item_value
    


currentItem = currentListing.getDefinedDataAt(currentSelection.getMinAddress())


import json
path = askFile("Where to store data", "OK")
with open(str(path), "w") as f:
  #f.write(repr(parse_item(currentItem)))
  f.write(json.dumps(parse_item(currentItem)))

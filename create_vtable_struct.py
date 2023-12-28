# Create a vtable struct for the current selection

#@category C++

def create_empty_signature(func):
  assert func
  si = func.signature
  assert "undefined" not in func.returnType.name, "%s has an undefined return type" % si.name
  for arg in si.arguments:
    assert "undefined" not in arg.dataType.name, "%s has an undefined argument" % si.name
    arg.name = ""
  return si


def iterate_range(r):
  addr = r.minAddress
  dat = getDataAt(addr)
  while dat.address < r.maxAddress:
    assert dat.pointer
    funcAddr = dat.value
    func = getFunctionAt(funcAddr)
    signature = create_empty_signature(func)
    print "%s -> %s"(signature, func.callingConventionName)
    dat = getDataAfter(dat)


iterate_range(currentSelection.firstRange)


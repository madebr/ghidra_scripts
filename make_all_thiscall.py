# Change all function pointers in range to __thiscall

#@category C++

import ghidra
try:
    from ghidra.ghidra_builtins import *
except ImportError:
    pass


# def create_empty_signature(func):
#   assert func
#   si = func.signature
#   assert "undefined" not in func.returnType.name, "%s has an undefined return type" % si.name
#   for arg in si.arguments:
#     assert "undefined" not in arg.dataType.name, "%s has an undefined argument" % si.name
#     arg.name = ""
#   return si


def set_function_to_thiscall(r, class_name):
  # r: hidra.program.util.ProgramSelection
  # class_name: str
  addr = r.minAddress
  dat = getDataAt(addr)
  while dat.address < r.maxAddress:
    assert dat.pointer
    funcAddr = dat.value
    func = getFunctionAt(funcAddr)
    if func:
      funcName = func.name
    else:
      funcName = "FUN_{}".format(dat.value)
      createFunction(funcAddr, "FUN_{}".format(dat.value))
      func = getFunctionAt(funcAddr)

    if func.callingConventionName == "__stdcall":
      # convert stdcall to __thiscall
      func.setCallingConvention("__thiscall")
    elif func.callingConventionName == "__fastcall":
      print("__fastcall detected... at {}".format(funcAddr))
      original_parameters = func.parameters
      print(original_parameters)
      func.removeParameter(0)
      func.setCallingConvention("__thiscall")
    elif func.callingConventionName == "__thiscall":
      pass # thiscall is okay!
    else:
      print("UNKNOWN convention at {}: {}".format(funcAddr, func.callingConventionName))

    if class_name:
      comm = getPlateComment(funcAddr) or ""
      lines = [l.strip(" \n\t:") for l in comm.splitlines()]
      if class_name not in lines:
        setPlateComment(funcAddr, comm + "\n" + class_name)

    dat = getDataAfter(dat)


def main():
    try:
        class_name= askString("Class name", "name")
    except ghidra.util.exception.CancelledException:
        class_name = None

    set_function_to_thiscall(currentSelection.firstRange, class_name)

main()
